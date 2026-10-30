#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <limits>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
#include <omp.h>

extern "C" {
struct HzParameters {
    int32_t metric, dtype, mode, steps, field_limit, threads;
    double alpha, eps, lam, commit_margin, route_mix, retention_mix;
};
}
namespace {
thread_local std::string last_error;
enum Stat { Witness, RetentionEvents, Commits, Appends, Candidates, Seeds, Extra,
            Failures, Routes, Shift, ScoreRegressions, ScoreReads, OutputChecks, StatCount };
using Stats = std::array<double, StatCount>;
float norm(const float* x, int d) {
    float sum=0;
    #pragma omp simd reduction(+:sum)
    for(int j=0;j<d;++j) sum+=x[j]*x[j];
    return std::sqrt(sum);
}
void unit(std::vector<float>& x) {
    const float n=norm(x.data(),int(x.size()));
    if(n>1e-12f) {
        #pragma omp simd
        for(size_t j=0;j<x.size();++j) x[j]/=n;
    } else std::fill(x.begin(),x.end(),0.0f);
}
float dot(const float* a,const float* b,int d) {
    float s=0;
    #pragma omp simd reduction(+:s)
    for(int j=0;j<d;++j) s+=a[j]*b[j];
    return s;
}
struct Query {
    std::vector<int64_t> ids, seed_ids;
    std::vector<float> raw, memories, original, cue, evidence, checkpoint;
    std::vector<double> scores, seed_top;
    std::vector<int> field;
    int locked=-1;
    Stats stats{};
};
struct Batch {
    const void* bank;
    int64_t nb;
    int d, k;
    HzParameters p;
    std::vector<Query> qs;
    std::vector<std::string> errors;
    float value(int64_t id,int j) const {
        const size_t pos=size_t(id)*size_t(d)+size_t(j);
        if(p.dtype==0) return static_cast<const float*>(bank)[pos];
        if(p.dtype==1) return float(static_cast<const uint8_t*>(bank)[pos]);
        return float(static_cast<const int8_t*>(bank)[pos]);
    }
    std::vector<float> read(int64_t id) const {
        std::vector<float> x(d);
        for(int j=0;j<d;++j) {
            x[j]=value(id,j);
            if(!std::isfinite(x[j])) throw std::runtime_error("Nonfinite candidate vector");
        }
        return x;
    }
    double score(const float* a,const Query& q) const {
        double s=0,an=0,qn=0;
        if(p.metric==0) {
            #pragma omp simd reduction(+:s)
            for(int j=0;j<d;++j) {double z=double(a[j])-q.original[j];s-=z*z;}
            return s;
        }
        #pragma omp simd reduction(+:s,an,qn)
        for(int j=0;j<d;++j) {
            double av=a[j], bv=q.original[j];s+=av*bv;an+=av*av;qn+=bv*bv;
        }
        if(p.metric==2) return an>0 && qn>0 ? s/(std::sqrt(an)*std::sqrt(qn)) : 0;
        return s;
    }
    bool better(const Query& q,int a,int b) const {
        if(q.scores[a]!=q.scores[b]) return q.scores[a]>q.scores[b];
        return q.ids[a]<q.ids[b];
    }
    std::vector<int> ordered(const Query& q,int take) const {
        std::vector<int> order(q.ids.size());std::iota(order.begin(),order.end(),0);
        const int n=std::min(take,int(order.size()));
        std::partial_sort(order.begin(),order.begin()+n,order.end(),[&](int a,int b){return better(q,a,b);});
        order.resize(n);return order;
    }
    void refresh(Query& q) const {
        q.evidence.resize(q.scores.size());
        if(p.metric==0) {
            for(size_t i=0;i<q.scores.size();++i) q.evidence[i]=float(1.0/(1.0+std::max(-q.scores[i],0.0)));
        } else {
            auto extremes=std::minmax_element(q.scores.begin(),q.scores.end());
            const double low=*extremes.first, span=*extremes.second-low;
            for(size_t i=0;i<q.scores.size();++i) q.evidence[i]=span>0 ? float((q.scores[i]-low)/span) : 1.0f;
        }
        q.field.resize(q.ids.size());std::iota(q.field.begin(),q.field.end(),0);
        int count=std::min(int(q.field.size()),p.field_limit);
        std::partial_sort(q.field.begin(),q.field.begin()+count,q.field.end(),[&](int a,int b){
            return q.evidence[a]!=q.evidence[b] ? q.evidence[a]>q.evidence[b] : a<b;
        });
        q.field.resize(count);
    }
    void add(Query& q,int64_t id,std::vector<float> x,double s) const {
        q.ids.push_back(id);q.scores.push_back(s);
        q.raw.insert(q.raw.end(),x.begin(),x.end());
        unit(x);q.memories.insert(q.memories.end(),x.begin(),x.end());
    }
    bool verify(Query& q,int index,const std::vector<float>& state) const {
        ++q.stats[Witness];
        const bool accepted=index>=0 && size_t(index)<q.ids.size() && state.size()==size_t(d) &&
            std::equal(state.begin(),state.end(),q.memories.begin()+size_t(index)*d);
        if(!accepted) {++q.stats[Failures];return false;}
        const std::vector<float> observed(q.memories.begin()+size_t(index)*d,q.memories.begin()+size_t(index+1)*d);
        if(observed!=state) {++q.stats[Failures];return false;}
        return true;
    }
    std::vector<float> state(const Query& q,int i) const {
        return {q.memories.begin()+size_t(i)*d,q.memories.begin()+size_t(i+1)*d};
    }
    void initialize(int qi,const float* query,const int64_t* seeds,int count) {
        Query& q=qs[qi];q.original.assign(query,query+d);q.cue=q.original;unit(q.cue);
        std::vector<int64_t> ids;
        for(int i=0;i<count;++i) if(seeds[i]>=0 && seeds[i]<nb) ids.push_back(seeds[i]);
        std::sort(ids.begin(),ids.end());ids.erase(std::unique(ids.begin(),ids.end()),ids.end());
        if(ids.size()<size_t(k)) throw std::runtime_error("FAISS returned fewer than k valid seed IDs; increase nprobe");
        q.ids.reserve(ids.size());q.raw.reserve(size_t(d)*ids.size());q.memories.reserve(size_t(d)*ids.size());
        for(int64_t id:ids) {auto x=read(id);double s=score(x.data(),q);add(q,id,std::move(x),s);}
        q.stats[ScoreReads]=ids.size();q.stats[Seeds]=ids.size();q.seed_ids=ids;
        for(int i:ordered(q,k)) q.seed_top.push_back(q.scores[i]);
        if(p.mode!=1 && p.mode!=4) {
            refresh(q);q.locked=ordered(q,1)[0];q.checkpoint=state(q,q.locked);
            if(!verify(q,q.locked,q.checkpoint)) throw std::runtime_error("Initial checkpoint failed witness verification");
        }
    }
    std::vector<float> refine(const Query& q) const {
        for(size_t i=0;i<q.ids.size();++i) {
            if(std::equal(q.original.begin(),q.original.end(),q.memories.begin()+i*d)) return state(q,int(i));
        }
        std::vector<float> x=q.cue;
        if(norm(x.data(),d)<=1e-12f) {
            double total=0;for(int i:q.field) total+=std::max(double(q.evidence[i]),0.0);
            for(int i:q.field) {
                float w=total>1e-12 ? float(std::max(double(q.evidence[i]),0.0)/total) : 1.0f/float(q.field.size());
                const float* m=q.memories.data()+size_t(i)*d;
                #pragma omp simd
                for(int j=0;j<d;++j) x[j]+=w*m[j];
            }
            unit(x);
        }
        int steps=p.mode==2 ? 0:p.steps;
        std::vector<float> field(d),responses(q.field.size());
        for(int step=0;step<steps;++step) {
            float denominator=0;
            for(size_t i=0;i<q.field.size();++i) {
                float h=dot(q.memories.data()+size_t(q.field[i])*d,x.data(),d);
                responses[i]=std::tanh(h)+float(p.alpha)*std::tanh(2.0f*h);
                denominator+=std::abs(responses[i]);
            }
            std::fill(field.begin(),field.end(),0);
            for(size_t i=0;i<q.field.size();++i) {
                const float* m=q.memories.data()+size_t(q.field[i])*d;const float r=responses[i];
                #pragma omp simd
                for(int j=0;j<d;++j) field[j]+=r*m[j];
            }
            float divisor=denominator+1e-12f;
            #pragma omp simd
            for(int j=0;j<d;++j) x[j]=float(1.0-p.lam)*x[j]+float(p.eps)*(field[j]/divisor);
            unit(x);
        }
        return x;
    }
    void route(int qi,float* output) {
        Query& q=qs[qi];
        if(p.mode==1 || p.mode==4) {std::copy(q.original.begin(),q.original.end(),output);return;}
        auto refined=refine(q);std::vector<float> routed=refined;
        ++q.stats[Routes];double shift=0;
        for(int j=0;j<d;++j) {double z=double(refined[j])-q.cue[j];shift+=z*z;}
        q.stats[Shift]+=std::sqrt(shift);
        if(p.mode!=3) {
            ++q.stats[RetentionEvents];float best=-std::numeric_limits<float>::infinity(),second=best;int winner=-1;
            for(size_t i=0;i<q.ids.size();++i) {
                float s=dot(q.memories.data()+i*d,refined.data(),d);
                if(s>best) {second=best;best=s;winner=int(i);} else if(s>second) second=s;
            }
            double margin=q.ids.size()==1 ? std::numeric_limits<double>::infinity():double(best)-second;
            if(margin>=p.commit_margin) {
                auto proposal=state(q,winner);
                if(!verify(q,winner,proposal)) throw std::runtime_error("Proposed checkpoint failed verification");
                q.locked=winner;q.checkpoint=std::move(proposal);++q.stats[Commits];
            }
            if(!verify(q,q.locked,q.checkpoint)) throw std::runtime_error("Retained checkpoint failed verification");
            for(int j=0;j<d;++j) routed[j]=float(1.0-p.retention_mix)*refined[j]+float(p.retention_mix)*q.checkpoint[j];
            unit(routed);
        }
        for(int j=0;j<d;++j) routed[j]=float(1.0-p.route_mix)*q.cue[j]+float(p.route_mix)*routed[j];
        unit(routed);float amplitude=norm(q.original.data(),d);
        for(int j=0;j<d;++j) output[j]=routed[j]*amplitude;
    }
    void expand(int qi,const int64_t* candidates,int count,int allowance) {
        Query& q=qs[qi];std::vector<int64_t> ids;
        for(int i=0;i<count;++i) if(candidates[i]>=0 && candidates[i]<nb) ids.push_back(candidates[i]);
        std::sort(ids.begin(),ids.end());ids.erase(std::unique(ids.begin(),ids.end()),ids.end());
        std::vector<int64_t> existing=q.ids;std::sort(existing.begin(),existing.end());
        std::vector<std::pair<int64_t,double>> extra;
        for(int64_t id:ids) if(!std::binary_search(existing.begin(),existing.end(),id)) {
            auto x=read(id);extra.emplace_back(id,score(x.data(),q));++q.stats[ScoreReads];
        }
        const size_t take=std::min(extra.size(),size_t(allowance));
        std::partial_sort(extra.begin(),extra.begin()+take,extra.end(),[](auto a,auto b){return a.second!=b.second ? a.second>b.second:a.first<b.first;});
        extra.resize(take);std::sort(extra.begin(),extra.end(),[](auto a,auto b){return a.first<b.first;});
        std::vector<float> previous;
        if(p.mode!=1 && p.mode!=4 && take) {
            previous=q.memories;
        }
        for(auto item:extra) add(q,item.first,read(item.first),item.second);
        if(p.mode!=1 && p.mode!=4 && take) {
            ++q.stats[Appends];
            if(!std::equal(previous.begin(),previous.end(),q.memories.begin())) {++q.stats[Failures];throw std::runtime_error("Appending candidates changed existing normalized memories");}
            refresh(q);
            if(!verify(q,q.locked,q.checkpoint)) throw std::runtime_error("Append invalidated the retained checkpoint");
        }
    }
    void finish(int qi,int32_t* output) {
        Query& q=qs[qi];auto order=ordered(q,k);
        if(order.size()!=size_t(k)) throw std::runtime_error("Incomplete candidate output");
        std::vector<int64_t> sorted=q.ids;std::sort(sorted.begin(),sorted.end());
        if(std::adjacent_find(sorted.begin(),sorted.end())!=sorted.end()) throw std::runtime_error("Duplicate candidate ID");
        for(int64_t id:q.seed_ids) if(!std::binary_search(sorted.begin(),sorted.end(),id)) throw std::runtime_error("Seed candidate lost during expansion");
        for(int rank=0;rank<k;++rank) {
            int i=order[rank];
            if(q.scores[i]<q.seed_top[rank]-1e-12) {++q.stats[ScoreRegressions];throw std::runtime_error("Original-metric score regressed");}
            const float* stored=q.raw.data()+size_t(i)*d;
            for(int j=0;j<d;++j) if(value(q.ids[i],j)!=stored[j]) {++q.stats[Failures];throw std::runtime_error("Output global ID disagrees with its stored record");}
            ++q.stats[OutputChecks];
            if(p.mode!=1 && p.mode!=4) {
                auto locked=state(q,i);
                if(!verify(q,i,locked)) throw std::runtime_error("Final stored state failed verification");
            }
            if(q.ids[i]>std::numeric_limits<int32_t>::max()) throw std::runtime_error("Official HDF5 int32 neighbour ID overflow");
            output[rank]=int32_t(q.ids[i]);
        }
        q.stats[Candidates]=q.ids.size();q.stats[Extra]=q.ids.size()-q.seed_ids.size();
    }
    template<class F> void parallel(F fn) {
        std::fill(errors.begin(),errors.end(),std::string());
        #pragma omp parallel for num_threads(p.threads) schedule(static)
        for(int qi=0;qi<int(qs.size());++qi) {
            try {fn(qi);} catch(const std::exception& e) {errors[qi]=e.what();} catch(...) {errors[qi]="Unknown native error";}
        }
        for(size_t i=0;i<errors.size();++i) if(!errors[i].empty()) throw std::runtime_error("Query "+std::to_string(i)+": "+errors[i]);
    }
};
}
extern "C" {
const char* hz_error() {return last_error.c_str();}
int hz_abi_version() {return 3;}
void* hz_create(const void* bank,int64_t nb,int32_t d,const float* queries,int32_t nq,
                const int64_t* seeds,int32_t seed_count,int32_t k,const HzParameters* parameters) {
    try {
        if(!bank || !queries || !seeds || !parameters || nb<1 || d<1 || nq<1 || seed_count<1 || k<1 || k>nb) throw std::runtime_error("Invalid native input sizes");
        const auto& p=*parameters;
        if(p.metric<0 || p.metric>2 || p.dtype<0 || p.dtype>2 || p.mode<0 || p.mode>4 || p.steps<0 || p.field_limit<1 || p.threads<1) throw std::runtime_error("Invalid native parameter counts");
        for(double v:{p.alpha,p.eps,p.lam,p.commit_margin,p.route_mix,p.retention_mix}) if(!std::isfinite(v)) throw std::runtime_error("Nonfinite native parameters");
        if(p.alpha<0 || p.eps<0 || p.lam<0 || p.lam>1 || p.commit_margin<0 || p.route_mix<0 || p.route_mix>1 || p.retention_mix<0 || p.retention_mix>1) throw std::runtime_error("Invalid native parameter ranges");
        auto b=std::make_unique<Batch>();b->bank=bank;b->nb=nb;b->d=d;b->k=k;b->p=p;b->qs.resize(nq);b->errors.resize(nq);
        b->parallel([&](int i){b->initialize(i,queries+size_t(i)*d,seeds+size_t(i)*seed_count,seed_count);});
        return b.release();
    } catch(const std::exception& e) {last_error=e.what();return nullptr;}
}
int hz_route(void* ptr,float* output) {
    try {if(!ptr || !output) throw std::runtime_error("Null route input");auto& b=*static_cast<Batch*>(ptr);b.parallel([&](int i){b.route(i,output+size_t(i)*b.d);});return 0;}
    catch(const std::exception& e){last_error=e.what();return -1;}
}
int hz_expand(void* ptr,const int64_t* candidates,int32_t count,int32_t allowance) {
    try {if(!ptr || !candidates || count<1 || allowance<0) throw std::runtime_error("Invalid expansion input");auto& b=*static_cast<Batch*>(ptr);b.parallel([&](int i){b.expand(i,candidates+size_t(i)*count,count,allowance);});return 0;}
    catch(const std::exception& e){last_error=e.what();return -1;}
}
int hz_finish(void* ptr,int32_t* output,double* statistics) {
    try {if(!ptr || !output || !statistics) throw std::runtime_error("Null finish input");auto& b=*static_cast<Batch*>(ptr);b.parallel([&](int i){b.finish(i,output+size_t(i)*b.k);});std::fill(statistics,statistics+StatCount,0.0);for(const auto& q:b.qs)for(int j=0;j<StatCount;++j)statistics[j]+=q.stats[j];return 0;}
    catch(const std::exception& e){last_error=e.what();return -1;}
}
void hz_destroy(void* ptr){delete static_cast<Batch*>(ptr);}
}
