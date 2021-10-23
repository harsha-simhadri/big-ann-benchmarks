#pragma once

#include <list>
#include <atomic>
#include <random>
#include <cassert>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>

#include <stdint.h>
#include <stdlib.h>

#include <unistd.h>

#include "hnswlib.h"
#include "visited_list_pool.h"

namespace hnswlib {

typedef uint32_t tableint;
typedef uint32_t linklistsizeint;
typedef uint8_t levelint;

template <typename Tdist>
class HierarchicalNSW : public AlgorithmInterface<Tdist> {

private:
    static const tableint max_update_element_locks = 65536;
    static const linklistsizeint DELETE_MARK = 1UL << (sizeof(linklistsizeint) * 8 - 1);

    size_t d_;
    size_t M_;
    size_t maxM_;
    size_t maxM0_;
    size_t ef_construction_;
    float repair_ratio_;

    size_t raw_data_size_;
    size_t data_size_;
    size_t size_links_level0_;
    size_t size_data_per_element_;
    size_t size_links_per_element_;
    size_t offsetData_;
    size_t label_offset_;

    double mult_;
    int maxlevel_;
    tableint enterpoint_node_;

    VPFUNC vp_func_;
    DISTFUNC<Tdist> dist_func_;
    DISTFUNC<Tdist> st_dist_func_;

    size_t max_elements_;
    size_t cur_element_count_;
    std::mutex cur_element_count_guard_;
    std::mutex global_;

    Level0StorageInterface* level0_storage_;
    char* level0_raw_memory_;
    char** linkLists_;
    levelint* element_levels_;

    std::atomic<bool>* link_list_locks_;
    // Locks to prevent race condition during update/insert of an element at same time.
    // Note: Locks for additions can also be used to prevent this race condition if the querying of KNN is not exposed along with update/inserts i.e multithread insert/update/query in parallel.
    std::vector<std::mutex> link_list_update_locks_;

    bool has_deletions_;
    std::unordered_map<labeltype, tableint> label_lookup_;

    std::vector<tableint> deleted_;
    std::vector<tableint> recycled_;
    std::unordered_set<tableint> repairing_;

    std::default_random_engine level_generator_;
    std::default_random_engine update_probability_generator_;

    size_t ef_;
    VisitedListPool* visited_list_pool_;

    struct SpinLock {
        std::atomic<bool>* lock;

        SpinLock(std::atomic<bool>* lock): lock(lock) {
            while(true) {
                bool val = false;
                if(lock->compare_exchange_weak(val, true)) {
                    break;
                }
            }
        }

        ~SpinLock() {
            bool val = true;
            bool ret = lock->compare_exchange_strong(val, false);
            assert(ret);
        }
    };

    struct CompareByFirst {
        constexpr bool operator()(const std::pair<Tdist, tableint>& a,
                                    const std::pair<Tdist, tableint>& b) const noexcept {
            return a.first < b.first;
        }
    };

public:
    mutable std::atomic<uint64_t> metric_hops;
    mutable std::atomic<uint64_t> metric_distance_computations;

private:
    inline labeltype* getExternalLabeLp(tableint internal_id) const {
        return (labeltype*)(level0_raw_memory_ + internal_id * size_data_per_element_ + label_offset_);
    }

    inline labeltype getExternalLabel(tableint internal_id) const {
        return *getExternalLabeLp(internal_id);
    }
public:
    inline void setExternalLabel(tableint internal_id, labeltype label) {
        *getExternalLabeLp(internal_id) = label;
    }

    inline char* getDataByInternalId(tableint internal_id) const {
        return level0_raw_memory_ + internal_id * size_data_per_element_ + offsetData_;
    }
private:
    inline linklistsizeint* getLinklist0(tableint internal_id) const {
        return (linklistsizeint*)(level0_raw_memory_ + internal_id * size_data_per_element_);
    };

    inline linklistsizeint* getLinklistN(tableint internal_id, int level) const {
        return (linklistsizeint*)(linkLists_[internal_id] + (level - 1) * size_links_per_element_);
    };

    inline linklistsizeint* getLinklist(tableint internal_id, int level) const {
        return level == 0 ? getLinklist0(internal_id) : getLinklistN(internal_id, level);
    };

    inline linklistsizeint getListCount(linklistsizeint* ptr) const {
        return *ptr & (~DELETE_MARK);
    }

    inline void setListCount(linklistsizeint* ptr, linklistsizeint size) {
        *ptr = (*ptr & DELETE_MARK) | (size & ~DELETE_MARK);
    }

    inline bool isMarkedDeleted(tableint internal_id) const {
        linklistsizeint* ptr = getLinklist0(internal_id);
        return (*ptr & DELETE_MARK) != 0;
    }

    inline void markDeleted(tableint internal_id) {
        linklistsizeint* ptr = getLinklist0(internal_id);
        *ptr |= DELETE_MARK;
    }

    int getRandomLevel(double reverse_size) {
        std::uniform_real_distribution<double> distribution(0.0, 1.0);
        double r = -log(distribution(level_generator_)) * reverse_size;
        return (int)r;
    }

    std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst>
    searchBaseLayer(tableint ep_id, const void* data_point, int layer) {
        VisitedList *vl = visited_list_pool_->getFreeVisitedList();
        vl_type *visited_array = vl->getArray();
        vl_type visited_array_tag = vl->getTag();

        std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> top_candidates;
        std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> candidateSet;

        Tdist lowerBound;
        if(!isMarkedDeleted(ep_id)) {
            Tdist dist = dist_func_(data_point, getDataByInternalId(ep_id), d_);
            top_candidates.emplace(dist, ep_id);
            lowerBound = dist;
            candidateSet.emplace(-dist, ep_id);
        }
        else {
            lowerBound = std::numeric_limits<Tdist>::max();
            candidateSet.emplace(-lowerBound, ep_id);
        }
        visited_array[ep_id] = visited_array_tag;

        while(!candidateSet.empty()) {
            std::pair<Tdist, tableint> curr_el_pair = candidateSet.top();
            if((-curr_el_pair.first) > lowerBound) {
                break;
            }
            candidateSet.pop();

            tableint curNodeNum = curr_el_pair.second;

            SpinLock lock(link_list_locks_ + curNodeNum);

            linklistsizeint* list = getLinklist(curNodeNum, layer);
            linklistsizeint size = getListCount(list);
            tableint* links = (tableint*)(list + 1);

            for(linklistsizeint j = 0; j < size; j++) {
                tableint candidate_id = links[j];
                if(visited_array[candidate_id] == visited_array_tag) {
                    continue;
                }
                visited_array[candidate_id] = visited_array_tag;
                char* currObj1 = getDataByInternalId(candidate_id);
                Tdist dist1 = dist_func_(data_point, currObj1, d_);
                if(top_candidates.size() < ef_construction_ || lowerBound > dist1) {
                    candidateSet.emplace(-dist1, candidate_id);
                    if(!isMarkedDeleted(candidate_id)) {
                        top_candidates.emplace(dist1, candidate_id);
                    }
                    if(top_candidates.size() > ef_construction_) {
                        top_candidates.pop();
                    }
                    if(!top_candidates.empty()) {
                        lowerBound = top_candidates.top().first;
                    }
                }
            }
        }

        visited_list_pool_->releaseVisitedList(vl);
        return top_candidates;
    }

    template <bool has_deletions, bool collect_metrics = false>
    std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst>
    searchBaseLayerST(tableint ep_id, const void* data_point, size_t ef) const {
        VisitedList *vl = visited_list_pool_->getFreeVisitedList();
        vl_type *visited_array = vl->getArray();
        vl_type visited_array_tag = vl->getTag();

        std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> top_candidates;
        std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> candidate_set;

        Tdist lowerBound;
        if(!has_deletions || !isMarkedDeleted(ep_id)) {
            Tdist dist = st_dist_func_(data_point, getDataByInternalId(ep_id), d_);
            lowerBound = dist;
            top_candidates.emplace(dist, ep_id);
            candidate_set.emplace(-dist, ep_id);
        }
        else {
            lowerBound = std::numeric_limits<Tdist>::max();
            candidate_set.emplace(-lowerBound, ep_id);
        }
        visited_array[ep_id] = visited_array_tag;

        uint32_t hops = 0, distance_computations = 0;
        while(!candidate_set.empty()) {
            std::pair<Tdist, tableint> current_node_pair = candidate_set.top();
            if((-current_node_pair.first) > lowerBound) {
                break;
            }
            candidate_set.pop();

            tableint current_node_id = current_node_pair.second;
            linklistsizeint* list = getLinklist0(current_node_id);
            linklistsizeint size = getListCount(list);
            if(collect_metrics) {
                hops++;
                distance_computations += size;
            }
            tableint* links = (tableint*)(list + 1);
#ifdef USE_SSE
            _mm_prefetch(visited_array + links[0], _MM_HINT_T0);
            _mm_prefetch(getDataByInternalId(links[0]), _MM_HINT_T0);
#endif
            for(linklistsizeint j = 0; j < size; j++) {
                tableint candidate_id = links[j];
#ifdef USE_SSE
                _mm_prefetch(visited_array + links[j + 1], _MM_HINT_T0);
                _mm_prefetch(getDataByInternalId(links[j + 1]), _MM_HINT_T0);
#endif
                if(!(visited_array[candidate_id] == visited_array_tag)) {
                    visited_array[candidate_id] = visited_array_tag;
                
                    char* currObj1 = getDataByInternalId(candidate_id);
                    Tdist dist = st_dist_func_(data_point, currObj1, d_);

                    if(top_candidates.size() < ef || lowerBound > dist) {
                        candidate_set.emplace(-dist, candidate_id);
#ifdef USE_SSE
                        _mm_prefetch(getDataByInternalId(candidate_set.top().second), _MM_HINT_T0);
#endif

                        if(!has_deletions || !isMarkedDeleted(candidate_id)) {
                            top_candidates.emplace(dist, candidate_id);
                        }
                        if(top_candidates.size() > ef) {
                            top_candidates.pop();
                        }
                        if(!top_candidates.empty()) {
                            lowerBound = top_candidates.top().first;
                        }
                    }
                }
            }
        }

        if(collect_metrics) {
            metric_hops += hops;
            metric_distance_computations += distance_computations;
        }

        visited_list_pool_->releaseVisitedList(vl);
        return top_candidates;
    }

    std::priority_queue<std::pair<Tdist, tableint>> searchKnnInternal(const void* query_data, int k) {
        std::priority_queue<std::pair<Tdist, tableint>> top_candidates;
        if(cur_element_count_ == 0) {
            return top_candidates;
        }
        tableint currObj = enterpoint_node_;
        Tdist curdist = st_dist_func_(query_data, getDataByInternalId(enterpoint_node_), d_);

        for(int level = maxlevel_; level > 0; level--) {
            bool changed = true;
            while(changed) {
                changed = false;
                linklistsizeint* list = getLinklistN(currObj, level);
                linklistsizeint size = getListCount(list);
                tableint* links = (tableint*)(list + 1);
                for(linklistsizeint i = 0; i < size; i++) {
                    tableint cand = links[i];
                    if(cand < 0 || cand > max_elements_) {
                        throw std::runtime_error("cand error");
                    }
                    Tdist d = st_dist_func_(query_data, getDataByInternalId(cand), d_);
                    if(d < curdist) {
                        curdist = d;
                        currObj = cand;
                        changed = true;
                    }
                }
            }
        }

        if(has_deletions_) {
            std::priority_queue<std::pair<Tdist, tableint>> top_candidates1 = searchBaseLayerST<true>(currObj,
                    query_data, ef_);
            top_candidates.swap(top_candidates1);
        }
        else {
            std::priority_queue<std::pair<Tdist, tableint>> top_candidates1 = searchBaseLayerST<false>(currObj,
                    query_data, ef_);
            top_candidates.swap(top_candidates1);
        }

        while(top_candidates.size() > k) {
            top_candidates.pop();
        }
        return top_candidates;
    };

    std::vector<tableint> getConnectionsWithLock(tableint internalId, int level) {
        SpinLock lock(link_list_locks_ + internalId);
        linklistsizeint* list = getLinklist(internalId, level);
        linklistsizeint size = getListCount(list);
        std::vector<tableint> result(size);
        tableint* links = (tableint*)(list + 1);
        memcpy(result.data(), links, size * sizeof(tableint));
        return result;
    };

    void getNeighborsByHeuristic2(
            std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst>& top_candidates,
            const size_t M) {
        if(top_candidates.size() < M) {
            return;
        }

        std::priority_queue<std::pair<Tdist, tableint>> queue_closest;
        std::vector<std::pair<Tdist, tableint>> return_list;
        while(top_candidates.size() > 0) {
            queue_closest.emplace(-top_candidates.top().first, top_candidates.top().second);
            top_candidates.pop();
        }

        while(queue_closest.size()) {
            if (return_list.size() >= M) {
                break;
            }
            std::pair<Tdist, tableint> curent_pair = queue_closest.top();
            Tdist Tdisto_query = -curent_pair.first;
            queue_closest.pop();
            bool good = true;

            for(std::pair<Tdist, tableint> second_pair : return_list) {
                Tdist curdist = dist_func_(getDataByInternalId(second_pair.second), getDataByInternalId(curent_pair.second), d_);
                if(curdist < Tdisto_query) {
                    good = false;
                    break;
                }
            }
            if(good) {
                return_list.push_back(curent_pair);
            }
        }

        for(std::pair<Tdist, tableint> curent_pair : return_list) {
            top_candidates.emplace(-curent_pair.first, curent_pair.second);
        }
    }

    tableint mutuallyConnectNewElement(const void */*data_point*/, tableint cur_c,
            std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> &top_candidates,
            int level, bool isUpdate) {
        size_t Mcurmax = level ? maxM_ : maxM0_;
        getNeighborsByHeuristic2(top_candidates, Mcurmax);
        if(top_candidates.size() > Mcurmax) {
            throw std::runtime_error("Should be not be more than M_ candidates returned by the heuristic");
        }

        std::vector<tableint> selectedNeighbors;
        selectedNeighbors.reserve(Mcurmax);
        while(top_candidates.size() > 0) {
            selectedNeighbors.push_back(top_candidates.top().second);
            top_candidates.pop();
        }

        tableint next_closest_entry_point = selectedNeighbors[0];

        {
            linklistsizeint* ll_cur = getLinklist(cur_c, level);
            if(!isUpdate && getListCount(ll_cur)) {
                throw std::runtime_error("The newly inserted element should have blank link list");
            }
            setListCount(ll_cur, selectedNeighbors.size());
            tableint* links = (tableint*)(ll_cur + 1);
            for(size_t idx = 0; idx < selectedNeighbors.size(); idx++) {
                if(!isUpdate && links[idx]) {
                    throw std::runtime_error("Possible memory corruption");
                }
                if(level > element_levels_[selectedNeighbors[idx]]) {
                    throw std::runtime_error("Trying to make a link on a non-existent level");
                }
                links[idx] = selectedNeighbors[idx];
            }
        }

        for(size_t idx = 0; idx < selectedNeighbors.size(); idx++) {
            SpinLock lock(link_list_locks_ + selectedNeighbors[idx]);

            linklistsizeint* ll_other = getLinklist(selectedNeighbors[idx], level);
            linklistsizeint sz_link_list_other = getListCount(ll_other);

            if(sz_link_list_other > Mcurmax) {
                throw std::runtime_error("Bad value of sz_link_list_other");
            }
            if(selectedNeighbors[idx] == cur_c) {
                throw std::runtime_error("Trying to connect an element to itself");
            }
            if(level > element_levels_[selectedNeighbors[idx]]) {
                throw std::runtime_error("Trying to make a link on a non-existent level");
            }

            tableint* links = (tableint*)(ll_other + 1);
            bool is_cur_c_present = false;
            if(isUpdate) {
                for(linklistsizeint j = 0; j < sz_link_list_other; j++) {
                    if(links[j] == cur_c) {
                        is_cur_c_present = true;
                        break;
                    }
                }
            }

            // If cur_c is already present in the neighboring connections of `selectedNeighbors[idx]` then no need to modify any connections or run the heuristics.
            if(!is_cur_c_present) {
                if(sz_link_list_other < Mcurmax) {
                    links[sz_link_list_other] = cur_c;
                    setListCount(ll_other, sz_link_list_other + 1);
                }
                else {
                    // finding the "weakest" element to replace it with the new one
                    Tdist d_max = dist_func_(getDataByInternalId(cur_c), getDataByInternalId(selectedNeighbors[idx]), d_);
                    // Heuristic:
                    std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> candidates;
                    candidates.emplace(d_max, cur_c);

                    for(linklistsizeint j = 0; j < sz_link_list_other; j++) {
                        Tdist dj = dist_func_(getDataByInternalId(links[j]), getDataByInternalId(selectedNeighbors[idx]), d_);
                        candidates.emplace(dj, links[j]);
                    }

                    getNeighborsByHeuristic2(candidates, Mcurmax);

                    linklistsizeint indx = 0;
                    while(candidates.size() > 0) {
                        links[indx] = candidates.top().second;
                        candidates.pop();
                        indx++;
                    }
                    setListCount(ll_other, indx);
                    // Nearest K:
                    /*int indx = -1;
                    for(linklistsizeint j = 0; j < sz_link_list_other; j++) {
                        Tdist dj = dist_func_(getDataByInternalId(links[j]), getDataByInternalId(selectedNeighbors[idx]), d_);
                        if(dj > d_max) {
                            indx = j;
                            d_max = d;
                        }
                    }
                    if(indx >= 0) {
                        links[indx] = cur_c;
                    } */
                }
            }
        }

        return next_closest_entry_point;
    }

    void repairConnectionsForUpdate(const void* dataPoint, tableint entryPointInternalId, tableint dataPointInternalId, int dataPointLevel, int maxLevel) {
        tableint currObj = entryPointInternalId;
        if(dataPointLevel < maxLevel) {
            Tdist curdist = dist_func_(dataPoint, getDataByInternalId(currObj), d_);
            for(int level = maxLevel; level > dataPointLevel; level--) {
                bool changed = true;
                while(changed) {
                    changed = false;
                    SpinLock lock(link_list_locks_ + currObj);
                    linklistsizeint* list = getLinklist(currObj, level);
                    linklistsizeint size = getListCount(list);
                    tableint* links = (tableint*)(list + 1);
#ifdef USE_SSE
                    _mm_prefetch(getDataByInternalId(links[0]), _MM_HINT_T0);
#endif
                    for(linklistsizeint i = 0; i < size; i++) {
#ifdef USE_SSE
                        _mm_prefetch(getDataByInternalId(links[i + 1]), _MM_HINT_T0);
#endif
                        tableint cand = links[i];
                        Tdist d = dist_func_(dataPoint, getDataByInternalId(cand), d_);
                        if(d < curdist) {
                            curdist = d;
                            currObj = cand;
                            changed = true;
                        }
                    }
                }
            }
        }

        if(dataPointLevel > maxLevel) {
            throw std::runtime_error("Level of item to be updated cannot be bigger than max level");
        }

        for(int level = dataPointLevel; level >= 0; level--) {
            std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> topCandidates = searchBaseLayer(
                    currObj, dataPoint, level);

            std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> filteredTopCandidates;
            while(topCandidates.size() > 0) {
                if(topCandidates.top().second != dataPointInternalId) {
                    filteredTopCandidates.push(topCandidates.top());
                }
                topCandidates.pop();
            }

            // Since element_levels_ is being used to get `dataPointLevel`, there could be cases where `topCandidates` could just contains entry point itself.
            // To prevent self loops, the `topCandidates` is filtered and thus can be empty.
            if(filteredTopCandidates.size() > 0) {
                bool epDeleted = isMarkedDeleted(entryPointInternalId);
                if(epDeleted) {
                    filteredTopCandidates.emplace(dist_func_(dataPoint, getDataByInternalId(entryPointInternalId), d_), entryPointInternalId);
                    if(filteredTopCandidates.size() > ef_construction_) {
                        filteredTopCandidates.pop();
                    }
                }

                currObj = mutuallyConnectNewElement(dataPoint, dataPointInternalId, filteredTopCandidates, level, true);
            }
        }
    }

    void updatePoint(const void* dataPoint, tableint internalId, float updateNeighborProbability) {
        // update the feature vector associated with existing point with new vector
        void* dst_data = getDataByInternalId(internalId);
        memcpy(dst_data, dataPoint, raw_data_size_);
        if(vp_func_) {
            vp_func_(dst_data, d_);
        }

        int maxLevelCopy = maxlevel_;
        tableint entryPointCopy = enterpoint_node_;
        // If point to be updated is entry point and graph just contains single element then just return.
        if(entryPointCopy == internalId && cur_element_count_ == 1) {
            return;
        }

        int elemLevel = element_levels_[internalId];
        std::uniform_real_distribution<float> distribution(0.0, 1.0);
        for(int layer = 0; layer <= elemLevel; layer++) {
            std::unordered_set<tableint> sCand;
            std::unordered_set<tableint> sNeigh;
            std::vector<tableint> listOneHop = getConnectionsWithLock(internalId, layer);
            if(listOneHop.size() == 0) {
                continue;
            }

            sCand.insert(internalId);

            for(auto&& elOneHop : listOneHop) {
                sCand.insert(elOneHop);

                if(distribution(update_probability_generator_) > updateNeighborProbability) {
                    continue;
                }

                sNeigh.insert(elOneHop);

                std::vector<tableint> listTwoHop = getConnectionsWithLock(elOneHop, layer);
                for(auto&& elTwoHop : listTwoHop) {
                    sCand.insert(elTwoHop);
                }
            }

            for(auto&& neigh : sNeigh) {
//                    if (neigh == internalId)
//                        continue;

                std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> candidates;
                int size = sCand.find(neigh) == sCand.end() ? sCand.size() : sCand.size() - 1;
                int elementsToKeep = std::min(int(ef_construction_), size);
                for(auto&& cand : sCand) {
                    if(cand == neigh) {
                        continue;
                    }

                    Tdist distance = dist_func_(getDataByInternalId(neigh), getDataByInternalId(cand), d_);
                    if(candidates.size() < elementsToKeep) {
                        candidates.emplace(distance, cand);
                    }
                    else {
                        if(distance < candidates.top().first) {
                            candidates.pop();
                            candidates.emplace(distance, cand);
                        }
                    }
                }

                // Retrieve neighbours using heuristic and set connections.
                getNeighborsByHeuristic2(candidates, layer == 0 ? maxM0_ : maxM_);

                {
                    SpinLock lock(link_list_locks_ + neigh);
                    linklistsizeint* list = getLinklist(neigh, layer);
                    size_t candSize = candidates.size();
                    setListCount(list, candSize);
                    tableint* links = (tableint*) (list + 1);
                    for(size_t idx = 0; idx < candSize; idx++) {
                        links[idx] = candidates.top().second;
                        candidates.pop();
                    }
                }
            }
        }

        repairConnectionsForUpdate(dataPoint, entryPointCopy, internalId, elemLevel, maxLevelCopy);
    };

    void loadIndex(const std::string& location, SpaceInterface<Tdist>* s, size_t max_elements_i = 0) {
        FILE* file = fopen(location.c_str (), "rb");
        if(!file) {
            throw std::runtime_error(std::string ("failed to open '").append (location).append ("'"));
        }
        loadIndex(file, s, max_elements_i);
        fclose(file);
    }

    void loadIndex(FILE* file, SpaceInterface<Tdist>* s, size_t max_elements_i = 0) {
        d_ = s->getDim();

        readBinaryPOD(file, M_);
        readBinaryPOD(file, maxM_);
        readBinaryPOD(file, maxM0_);
        readBinaryPOD(file, ef_construction_);
        readBinaryPOD(file, repair_ratio_);

        readBinaryPOD(file, maxlevel_);
        readBinaryPOD(file, max_elements_);
        readBinaryPOD(file, cur_element_count_);
        readBinaryPOD(file, enterpoint_node_);

        raw_data_size_ = s->getRawDataSize();
        data_size_ = s->getDataSize();
        size_links_level0_ = maxM0_ * sizeof(tableint) + sizeof(linklistsizeint);
        size_data_per_element_ = size_links_level0_ + data_size_ + sizeof(labeltype);
        size_links_per_element_ = maxM_ * sizeof(tableint) + sizeof(linklistsizeint);
        offsetData_ = size_links_level0_;
        label_offset_ = size_links_level0_ + data_size_;

        mult_ = 1 / log(1.0 * M_);

        vp_func_ = s->getVectorPreprocessFunc();
        dist_func_ = s->getDistFunc();
        st_dist_func_ = s->getDistFuncST();

        size_t max_elements=max_elements_i;
        if(max_elements < cur_element_count_) {
            max_elements = max_elements_;
        }
        max_elements_ = max_elements;

        link_list_locks_ = new std::atomic<bool> [max_elements_];
        for(size_t i = 0; i < max_elements_; i++) {
            link_list_locks_[i].store(false);
        }
        std::vector<std::mutex>(max_update_element_locks).swap(link_list_update_locks_);

        visited_list_pool_ = new VisitedListPool(1, max_elements);

        linkLists_ = (char**)malloc(sizeof(void*) * max_elements);
        if(linkLists_ == nullptr) {
            throw std::runtime_error("Not enough memory: loadIndex failed to allocate linklists");
        }
        element_levels_ = (levelint*)malloc(sizeof(levelint) * max_elements_);
        if(element_levels_ == nullptr) {
            throw std::runtime_error("out of memory"); 
        }
        ef_ = 10;
        for(size_t i = 0; i < cur_element_count_; i++) {
            size_t linkListSize;
            readBinaryPOD(file, linkListSize);
            if(linkListSize == 0) {
                element_levels_[i] = 0;
                linkLists_[i] = nullptr;
            }
            else {
                element_levels_[i] = linkListSize / size_links_per_element_;
                linkLists_[i] = (char*)malloc(linkListSize);
                if(linkLists_[i] == nullptr) {
                    throw std::runtime_error("Not enough memory: loadIndex failed to allocate linklist");
                }
                readBinary(file, linkLists_[i], linkListSize);
            }
        }

        long position = ftell (file);
        if (position < 0) {
            throw std::runtime_error("failed to get the current position of file");
        }
        size_t level0_offset = alignToPageSize(position);
        size_t level0_len = max_elements_ * size_data_per_element_;
        level0_raw_memory_ = (char*)level0_storage_->load(file, level0_offset, level0_len);
        if(fseek(file, alignToPageSize(level0_offset + level0_len), SEEK_SET) < 0) {
            throw std::runtime_error("failed to set current position of file");
        }

        has_deletions_ = false;
        for(size_t i = 0; i < cur_element_count_; i++) {
            if(isMarkedDeleted(i)) {
                has_deletions_ = true;
                deleted_.push_back(i);
            }
            else {
                label_lookup_[getExternalLabel(i)] = i;
            }
        }

        metric_hops.store(0);
        metric_distance_computations.store(0);

        delete s;
    }

    static size_t alignToPageSize(size_t offset) {
        size_t pgsize = getpagesize();
        size_t align_mod = offset % pgsize;
        return align_mod == 0 ? offset : offset + pgsize - align_mod;
    }

    static void writeBinary(FILE* file, const void* buf, size_t len) {
        if(fwrite(buf, 1, len, file) != len) {
            throw std::runtime_error("failed to write to file");
        }
    }

    template <typename T>
    static void writeBinaryPOD(FILE* file, const T &podRef) {
        writeBinary(file, &podRef, sizeof(T));
    }

    static void readBinary(FILE* file, void* buf, size_t len) {
        if(fread(buf, 1, len, file) != len) {
            throw std::runtime_error("failed to read from file");
        }
    }

    template <typename T>
    static void readBinaryPOD(FILE* file, T& podRef) {
        readBinary(file, &podRef, sizeof(T));
    }

public:
    HierarchicalNSW(SpaceInterface<Tdist>* s, Level0StorageInterface* level0_stroage, const std::string& location,
            size_t max_elements = 0) : level0_storage_(level0_stroage) {
        loadIndex(location, s, max_elements);
    }

    HierarchicalNSW(SpaceInterface<Tdist>* s, Level0StorageInterface* level0_stroage, FILE* file,
            size_t max_elements = 0) : level0_storage_(level0_stroage) {
        loadIndex(file, s, max_elements);
    }

    HierarchicalNSW(SpaceInterface<Tdist>* s, Level0StorageInterface* level0_stroage, size_t max_elements,
            size_t M = 16, size_t ef_construction = 200, size_t random_seed = 12345): level0_storage_(level0_stroage),
            link_list_update_locks_(max_update_element_locks), level_generator_(random_seed), update_probability_generator_(random_seed + 1) {
        d_ = s->getDim();
        M_ = M;
        maxM_ = M_;
        maxM0_ = M_ * 2;
        ef_construction_ = std::max(ef_construction, M_);
        repair_ratio_ = 0.5f;

        raw_data_size_ = s->getRawDataSize();
        data_size_ = s->getDataSize();
        size_links_level0_ = maxM0_ * sizeof(tableint) + sizeof(linklistsizeint);
        size_data_per_element_ = size_links_level0_ + data_size_ + sizeof(labeltype);
        size_links_per_element_ = maxM_ * sizeof(tableint) + sizeof(linklistsizeint);
        offsetData_ = size_links_level0_;
        label_offset_ = size_links_level0_ + data_size_;

        mult_ = 1 / log(1.0 * M_);
        maxlevel_ = -1;
        enterpoint_node_ = -1;

        vp_func_ = s->getVectorPreprocessFunc();
        dist_func_ = s->getDistFunc();
        st_dist_func_ = s->getDistFuncST();

        max_elements_ = max_elements;
        cur_element_count_ = 0;

        level0_raw_memory_ = (char*)level0_storage_->allocate(size_data_per_element_ * max_elements_);
        
        linkLists_ = (char**)malloc(sizeof(void*) * max_elements_);
        if(linkLists_ == nullptr) {
            throw std::runtime_error("out of memory");
        }
        element_levels_ = (levelint*)malloc(sizeof(levelint) * max_elements_);
        if(element_levels_ == nullptr) {
            throw std::runtime_error("out of memory"); 
        }
        memset(element_levels_, 0, sizeof(levelint) * max_elements_);

        link_list_locks_ = new std::atomic<bool> [max_elements_];
        for(size_t i = 0; i < max_elements_; i++) {
            link_list_locks_[i].store(false);
        }

        has_deletions_ = false;
        ef_ = 16;
        visited_list_pool_ = new VisitedListPool(1, max_elements_);
        metric_hops.store(0);
        metric_distance_computations.store(0);

        delete s;
    }

    ~HierarchicalNSW() {
        level0_storage_->free(level0_raw_memory_, max_elements_ * size_data_per_element_);
        delete level0_storage_;
        for(size_t i = 0; i < cur_element_count_; i++) {
            if(element_levels_[i] > 0) {
                free(linkLists_[i]);
            }
        }
        free(linkLists_);
        free(element_levels_);
        delete[] link_list_locks_;
        delete visited_list_pool_;
    }

    inline size_t getM() const {
        return M_;
    }

    inline size_t getEfConstruction() const {
        return ef_construction_;
    }

    inline void setEfConstruction(size_t ef) {
        ef_construction_ = ef;
    }

    inline float getRepairRatio() const {
        return repair_ratio_;
    }

    inline void setRepairRatio(float r) {
        repair_ratio_ = r;
    }

    inline size_t getEfSearch() const {
        return ef_;
    }

    inline void setEfSearch(size_t ef) {
        ef_ = ef;
    }

    inline size_t getMaxElement() const {
        return max_elements_;
    }

    inline size_t getElementCount() const {
        return cur_element_count_;
    }

    void resizeIndex(size_t new_max_elements) {
        if(new_max_elements < cur_element_count_) {
            throw std::runtime_error("cannot resize, new_max_elements < cur_element_count_");
        }
        void* level0_raw_memory_new = realloc(level0_raw_memory_, new_max_elements * size_data_per_element_);
        if(level0_raw_memory_new == nullptr) {
            throw std::runtime_error("out of memory");
        }
        level0_raw_memory_ = (char*)level0_raw_memory_new;
        void* linkLists_new = realloc(linkLists_, sizeof(void*) * new_max_elements);
        if(linkLists_new == nullptr) {
            throw std::runtime_error("out of memory");
        }
        linkLists_ = (char**)linkLists_new;
        void* element_levels_new = realloc(element_levels_, sizeof(levelint) * new_max_elements);
        if(element_levels_new == nullptr) {
            throw std::runtime_error("out of memory");
        }
        element_levels_ = (levelint*)element_levels_new;
        delete[] link_list_locks_;
        link_list_locks_ = new std::atomic<bool> [new_max_elements];
        for(size_t i = 0; i < new_max_elements; i++) {
            link_list_locks_[i].store(false);
        }
        delete visited_list_pool_;
        visited_list_pool_ = new VisitedListPool(1, new_max_elements);
        max_elements_ = new_max_elements;
    }

    void saveIndex(const std::string& location) const {
        FILE* file = fopen(location.c_str(), "wb");
        if(!file) {
            throw std::runtime_error(std::string("failed to open '").append(location).append("'"));
        }
        saveIndex(file);
        fclose(file);
    }

    void saveIndex(FILE* file) const {
        writeBinaryPOD(file, M_);
        writeBinaryPOD(file, maxM_);
        writeBinaryPOD(file, maxM0_);
        writeBinaryPOD(file, ef_construction_);
        writeBinaryPOD(file, repair_ratio_);

        writeBinaryPOD(file, maxlevel_);
        // somebody want to spare some disk space by not saving the used level0
        #ifdef SAVE_UNUSED_LEVEL0
        writeBinaryPOD(file, max_elements_);
        #else
        writeBinaryPOD(file, cur_element_count_);
        #endif

        writeBinaryPOD(file, cur_element_count_);
        writeBinaryPOD(file, enterpoint_node_);

        for(size_t i = 0; i < cur_element_count_; i++) {
            size_t linkListSize = element_levels_[i] > 0 ? size_links_per_element_ * element_levels_[i] : 0;
            writeBinaryPOD(file, linkListSize);
            if(linkListSize) {
                writeBinary(file, linkLists_[i], linkListSize);
            }
        }

        auto padding_to_pgsize = [&]() {
            long position = ftell(file);
            if(position < 0) {
                throw std::runtime_error("failed to get the current position of file");
            }
            size_t pgsize = getpagesize();
            size_t align_mod = position % pgsize;
            if(align_mod != 0) {
                size_t padding_len = pgsize - align_mod;
                char* padding = new char [padding_len];
                writeBinary(file, padding, padding_len);
                delete[] padding;
            }
        };
        padding_to_pgsize();
        #ifdef SAVE_UNUSED_LEVEL0
        writeBinary(file, level0_raw_memory_, max_elements_ * size_data_per_element_);
        #else
        writeBinary(file, level0_raw_memory_, cur_element_count_ * size_data_per_element_);
        #endif
        padding_to_pgsize();
    }

    void deletePoint(labeltype label) {
        std::unique_lock<std::mutex> lock(cur_element_count_guard_);
        auto search = label_lookup_.find(label);
        if(search == label_lookup_.end()) {
            throw std::runtime_error("Label not found");
        }
        tableint internal_id = search->second;
        label_lookup_.erase(search);
        markDeleted(internal_id);
        deleted_.push_back(internal_id);
        has_deletions_ = true;
    }

    inline size_t getDeletedCount() const {
        return deleted_.size();
    }

    void recycleDeletedPoints() {
        std::unique_lock<std::mutex> lock(cur_element_count_guard_);
        if(deleted_.empty()) {
            return;
        }

        if(isMarkedDeleted(enterpoint_node_)) {
            std::unique_lock<std::mutex> glock(global_);
            int alt_maxlevel = -1;
            tableint alt_enterpoint = -1;
            for(size_t i = 0; i < cur_element_count_; i++) {
                if(!isMarkedDeleted(i)) {
                    if(element_levels_[i] > alt_maxlevel) {
                        alt_maxlevel = element_levels_[i];
                        alt_enterpoint = i;
                    }
                }
            }
            maxlevel_ = alt_maxlevel;
            enterpoint_node_ = alt_enterpoint;
        }

        size_t repair_thresholdn = size_t(maxM_ * repair_ratio_);
        size_t repair_threshold0 = size_t(maxM0_ * repair_ratio_);

        for(size_t i = 0; i < cur_element_count_; i++) {
            SpinLock lock(link_list_locks_ + i);

            if(isMarkedDeleted(i)) {
                if(element_levels_[i] > 0) {
                    element_levels_[i] = 0;
                    free(linkLists_[i]);
                }
                continue;
            }

            bool need_repair = false;

            for(int level = element_levels_[i]; level >= 0; level--) {
                linklistsizeint* list = getLinklist(i, level);
                linklistsizeint size = getListCount(list);
                tableint* links = (tableint*)(list + 1);
                linklistsizeint new_size = 0;
                for(linklistsizeint j = 0; j < size; j++) {
                    if(!isMarkedDeleted(links[j])) {
                        if(new_size != j) {
                            links[new_size] = links[j];
                        }
                        new_size++;
                    }
                }
                assert(new_size <= size);
                if(new_size != size) {
                    setListCount(list, new_size);
                }
                if(new_size < (level > 0 ? repair_thresholdn : repair_threshold0)) {
                    need_repair = true;
                }
            }

            if(need_repair) {
                repairing_.insert(i);
            }
        }

        recycled_.insert(recycled_.end(), deleted_.begin(), deleted_.end());
        deleted_.clear();
        has_deletions_ = false;
    }

    inline size_t getRepairingCount() const {
        return repairing_.size();
    }

    size_t repairConnections(size_t npoint = 1) {
        std::vector<tableint> ids;
        std::unique_lock<std::mutex> lock(cur_element_count_guard_);
        npoint = std::min(npoint, repairing_.size());
        ids.reserve(npoint);
        for(size_t i = 0; i < npoint; i++) {
            auto it = repairing_.begin();
            ids.push_back(*it);
            repairing_.erase(it);
        }
        lock.unlock();

        tableint entryPointCopy = enterpoint_node_;
        int maxLevelCopy = maxlevel_;
        for(tableint id : ids) {
            repairConnectionsForUpdate(getDataByInternalId(id), entryPointCopy, id, element_levels_[id], maxLevelCopy);
        }
        return ids.size();
    }

    inline void addPoint(const void* data_point, labeltype label) {
        addPoint(data_point, label, -1);
    }

    tableint addPoint(const void* data_point, labeltype label, int level) {
        tableint cur_c = 0;
        {
            // Checking if the element with the same label already exists
            // if so, updating it *instead* of creating a new element.
            std::unique_lock<std::mutex> templock_curr(cur_element_count_guard_);
            auto search = label_lookup_.find(label);
            if(search != label_lookup_.end()) {
                tableint existingInternalId = search->second;

                templock_curr.unlock();

                std::unique_lock<std::mutex> lock_el_update(link_list_update_locks_[(existingInternalId & (max_update_element_locks - 1))]);
                updatePoint(data_point, existingInternalId, 1.0);
                return existingInternalId;
            }

            if(recycled_.empty()) {
                if(cur_element_count_ >= max_elements_) {
                    throw std::runtime_error("The number of elements exceeds the specified limit");
                }
                cur_c = cur_element_count_;
                cur_element_count_++;
            }
            else {
                cur_c = recycled_.back();
                recycled_.pop_back();
            }
            label_lookup_[label] = cur_c;
        }

        // Take update lock to prevent race conditions on an element with insertion/update at the same time.
        std::unique_lock<std::mutex> lock_el_update(link_list_update_locks_[(cur_c & (max_update_element_locks - 1))]);
        SpinLock lock_el(link_list_locks_ + cur_c);
        int curlevel = getRandomLevel(mult_);
        if(level > 0) {
            curlevel = level;
        }

        element_levels_[cur_c] = curlevel;

        std::unique_lock<std::mutex> templock(global_);
        int maxlevelcopy = maxlevel_;
        if(curlevel <= maxlevelcopy) {
            templock.unlock();
        }
        tableint currObj = enterpoint_node_;
        tableint enterpoint_copy = enterpoint_node_;

        memset(level0_raw_memory_ + cur_c * size_data_per_element_, 0, size_data_per_element_);

        // Initialisation of the data and label
        setExternalLabel(cur_c, label);
        void* dst_data = getDataByInternalId(cur_c);
        memcpy(dst_data, data_point, raw_data_size_);
        if(vp_func_) {
            vp_func_(dst_data, d_);
        }

        if(curlevel) {
            linkLists_[cur_c] = (char*)malloc(size_links_per_element_ * curlevel);
            if(linkLists_[cur_c] == nullptr) {
                throw std::runtime_error("Not enough memory: addPoint failed to allocate linklist");
            }
            memset(linkLists_[cur_c], 0, size_links_per_element_ * curlevel);
        }

        if((signed)currObj != -1) {

            if(curlevel < maxlevelcopy) {

                Tdist curdist = dist_func_(data_point, getDataByInternalId(currObj), d_);
                for(int level = maxlevelcopy; level > curlevel; level--) {
                    bool changed = true;
                    while (changed) {
                        changed = false;
                        SpinLock lock(link_list_locks_ + currObj);
                        linklistsizeint* list = getLinklistN(currObj, level);
                        linklistsizeint size = getListCount(list);
                        tableint* links = (tableint*)(list + 1);
                        for(linklistsizeint i = 0; i < size; i++) {
                            tableint cand = links[i];
                            if(cand < 0 || cand > max_elements_) {
                                throw std::runtime_error("cand error");
                            }
                            Tdist d = dist_func_(data_point, getDataByInternalId(cand), d_);
                            if(d < curdist) {
                                curdist = d;
                                currObj = cand;
                                changed = true;
                            }
                        }
                    }
                }
            }

            bool epDeleted = isMarkedDeleted(enterpoint_copy);
            for(int level = std::min(curlevel, maxlevelcopy); level >= 0; level--) {
                if(level > maxlevelcopy || level < 0) {
                    throw std::runtime_error("Level error");
                }

                std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> top_candidates = searchBaseLayer(
                        currObj, data_point, level);
                if(epDeleted) {
                    top_candidates.emplace(dist_func_(data_point, getDataByInternalId(enterpoint_copy), d_), enterpoint_copy);
                    if(top_candidates.size() > ef_construction_) {
                        top_candidates.pop();
                    }
                }
                currObj = mutuallyConnectNewElement(data_point, cur_c, top_candidates, level, false);
            }


        } else {
            // Do nothing for the first element
            enterpoint_node_ = 0;
            maxlevel_ = curlevel;
        }

        //Releasing lock for the maximum level
        if(curlevel > maxlevelcopy) {
            enterpoint_node_ = cur_c;
            maxlevel_ = curlevel;
        }
        return cur_c;
    };

    std::priority_queue<std::pair<Tdist, labeltype>> searchKnn(const void* query_data, size_t k) const {
        std::priority_queue<std::pair<Tdist, labeltype>> result;
        if(cur_element_count_ == 0) {
            return result;
        }

        tableint currObj = enterpoint_node_;
        Tdist curdist = st_dist_func_(query_data, getDataByInternalId(enterpoint_node_), d_);

        uint64_t hops = 0, distance_computations = 0, collect_metrics = false;
        for(int level = maxlevel_; level > 0; level--) {
            bool changed = true;
            while(changed) {
                changed = false;
                linklistsizeint* list = getLinklistN(currObj, level);
                linklistsizeint size = getListCount(list);
                if (collect_metrics) {
                    hops++;
                    distance_computations += size;
                }

                tableint* links = (tableint*)(list + 1);
                for(linklistsizeint i = 0; i < size; i++) {
                    tableint cand = links[i];
                    if(cand < 0 || cand > max_elements_) {
                        throw std::runtime_error("cand error");
                    }
                    Tdist d = st_dist_func_(query_data, getDataByInternalId(cand), d_);

                    if(d < curdist) {
                        curdist = d;
                        currObj = cand;
                        changed = true;
                    }
                }
            }
        }
        if (collect_metrics) {
            metric_hops += hops;
            metric_distance_computations += distance_computations;
        }

        std::priority_queue<std::pair<Tdist, tableint>, std::vector<std::pair<Tdist, tableint>>, CompareByFirst> top_candidates;
        if (has_deletions_ && collect_metrics) {
            top_candidates = searchBaseLayerST<true,true>(currObj, query_data, std::max(ef_, k));
        } else if (!has_deletions_ && collect_metrics) {
            top_candidates = searchBaseLayerST<false,true>(currObj, query_data, std::max(ef_, k));
        } else if (has_deletions_ && !collect_metrics) {
            top_candidates = searchBaseLayerST<true,false>(currObj, query_data, std::max(ef_, k));
        } else if (!has_deletions_ && !collect_metrics) {
            top_candidates = searchBaseLayerST<false,false>(currObj, query_data, std::max(ef_, k));
        }

        while (top_candidates.size() > k) {
            top_candidates.pop();
        }
        while (top_candidates.size() > 0) {
            std::pair<Tdist, tableint> rez = top_candidates.top();
            result.push(std::pair<Tdist, labeltype>(rez.first, getExternalLabel(rez.second)));
            top_candidates.pop();
        }
        return result;
    };

};

}
