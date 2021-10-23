#pragma once

#include <faiss/Index.h>
#include <faiss/hnswlib/hnswlib.h>
#include <faiss/impl/FaissAssert.h>


namespace faiss {

struct IndexHNSWlib : Index {

    float scale;
    float bias;

    IndexHNSWlib(size_t d, MetricType metric) : Index(d, metric), scale(1.0f), bias(0.0f) {
    }

    virtual ~IndexHNSWlib() {
    }

    virtual void setEFConstruction(size_t ef) = 0;

    virtual void setEFSearch(size_t ef) = 0;

    virtual size_t getEfConstruction() = 0;

    virtual size_t getEfSearch() = 0;

    virtual void save(FILE* file) const = 0;

    template <typename Tdist, typename Tcorr>
    static hnswlib::SpaceInterface<Tdist>* createSpace(size_t d, MetricType metric) {
       if(metric == METRIC_INNER_PRODUCT) {
            return new hnswlib::InnerProductSpace<Tdist, Tcorr>(d);
        }
        else if(metric == METRIC_L2) {
            return new hnswlib::L2Space<Tdist, Tcorr>(d);
        }
        else {
            FAISS_THROW_FMT("unsupported metric: %d", metric);
        }
    }

    template <typename T>
    const T* convertVector(size_t d, const float* x, T) const {
        T* tx = new T [d];
        for(size_t i = 0; i < d; i++) {
            tx[i] = T(x[i] * scale + bias);
        }
        return tx;
    }

    template <typename T>
    void  deconvertVector(size_t d, const T* x, float* fx) const{
        for(size_t i = 0 ; i < d; i++){
            fx[i] = ((float)x[i] - bias) / scale;
        }
    }


    template <typename T>
    inline void deleteConvertedVector(const T* tx) const {
        delete[] tx;
    }

    inline const float* convertVector(size_t, const float* x, float) const {
        return x;
    }

    // inline void deconvertVector(size_t, const float* x, float* fx) const{
    //     fx = x;
    // }

    inline void deleteConvertedVector(const float*) const {
    }

};

template <typename Tdist, typename Tcorr>
struct IndexHNSWlibImpl : IndexHNSWlib {

    const size_t INIT_MAX_ELEMENTS = 1UL << 20;

    hnswlib::HierarchicalNSW<Tdist>* hnsw;

    IndexHNSWlibImpl(size_t d, size_t M, MetricType metric = METRIC_L2) :
            IndexHNSWlib(d, metric) {
        hnsw = new hnswlib::HierarchicalNSW<Tdist>(createSpace<Tdist, Tcorr>(d, metric),
                new hnswlib::VmemLevel0, INIT_MAX_ELEMENTS, M);
    }

    IndexHNSWlibImpl(size_t d, FILE* file, MetricType metric = METRIC_L2) :
            IndexHNSWlib (d, metric) {
        hnswlib::Level0StorageInterface* storage;
        char* env_pmem = getenv("USE_PMEM");
        if(env_pmem && strcmp(env_pmem, "1") == 0) {
            storage = new hnswlib::PmemLevel0;
        }
        else {
            storage = new hnswlib::VmemLevel0;
        }
        hnsw = new hnswlib::HierarchicalNSW<Tdist>(createSpace<Tdist, Tcorr>(d, metric),
                storage, file);
    }

    ~IndexHNSWlibImpl() {
        delete hnsw;
    }

    void setEFConstruction(size_t ef) override {
        hnsw->setEfConstruction(ef);
    }

    void setEFSearch(size_t ef) override {
        hnsw->setEfSearch(ef);
    }

    size_t getEfConstruction() override{
        return hnsw->getEfConstruction();
    }

    size_t getEfSearch() override{
        return hnsw->getEfSearch();
    }

    void save(FILE* file) const {
        hnsw->saveIndex(file);
    }

    void add(idx_t n, const float* x) override {
        add_with_ids(n, x, nullptr);
    }

    void add_with_ids(idx_t n, const float* x, const idx_t* xids) override {
        size_t max_elements = hnsw->getMaxElement();
        bool need_resize = false;
        while(ntotal + n > max_elements) {
            need_resize = true;
            max_elements = size_t(max_elements * 1.5);
        }
        if(need_resize) {
            hnsw->resizeIndex(max_elements);
        }
        FAISS_ASSERT (ntotal + n <= hnsw->getMaxElement());
        #pragma omp parallel for
        for(idx_t i = 0; i < n; i++) {
            const float* xi = x + d * i;
            const Tcorr* txi = convertVector(d, xi, Tcorr());
            hnsw->addPoint(txi, xids ? xids[i] : ntotal + i);
            deleteConvertedVector(txi);
        }
        ntotal += n;
        if(verbose) {
            printf("%lu vectors newly added, now %lu totally\n", n, ntotal);
        }
    }

    void reset() override {
        size_t M = hnsw->getM();
        size_t ef_construction = hnsw->getEfConstruction();
        size_t ef_search = hnsw->getEfSearch();
        delete hnsw;
        hnsw = new hnswlib::HierarchicalNSW<Tdist>(createSpace<Tdist, Tcorr>(d, metric_type),
                new hnswlib::VmemLevel0, INIT_MAX_ELEMENTS, M, ef_construction);
        hnsw->setEfSearch(ef_search);
        ntotal = 0;
    }

    void reconstruct (idx_t key, float* recons) const override{

        Tcorr* temp = (Tcorr*)(hnsw->getDataByInternalId(key));
        deconvertVector(d, temp, recons);
    }

    void search(idx_t n, const float* x,
            idx_t k, float* distances, idx_t* labels) const override {
        #pragma omp parallel for
        for(idx_t i = 0; i < n; i++) {
            const float* xi = x + i * d;
            const Tcorr* txi = convertVector(d, xi, Tcorr());
            auto topk = hnsw->searchKnn(txi, k);
            deleteConvertedVector(txi);
            float* distances_i = distances + (i + 1) * k - 1;
            idx_t* labels_i = labels + (i + 1) * k - 1;
            for(idx_t j = 0; j < k; j++) {
                auto& entry = topk.top();
                *distances_i = float(entry.first);
                *labels_i = entry.second;
                distances_i--;
                labels_i--;
                topk.pop();
            }
        }
    }

};

using IndexHNSWlibFp32 = IndexHNSWlibImpl<float, float>;
using IndexHNSWlibBfp16 = IndexHNSWlibImpl<float, bfp16_t>;
using IndexHNSWlibInt16 = IndexHNSWlibImpl<int64_t, int16_t>;
using IndexHNSWlibInt8 = IndexHNSWlibImpl<int, int8_t>;

}
