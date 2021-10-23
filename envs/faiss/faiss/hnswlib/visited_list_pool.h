#pragma once

#include <mutex>

#include <stdint.h>
#include <string.h>

namespace hnswlib {

typedef uint16_t vl_type;

class VisitedList {

private:
    vl_type tag;
    vl_type* array;
    size_t numelements;

public:
    VisitedList(size_t numelements) : numelements(numelements) {
        tag = vl_type(-1);
        array = new vl_type[numelements];
    }

    void reset() {
        tag++;
        if(tag == 0) {
            memset(array, 0, numelements * sizeof(vl_type));
            tag++;
        }
    };

    inline vl_type getTag() const {
        return tag;
    }

    inline vl_type* getArray() const {
        return array;
    }

    ~VisitedList() {
        delete[] array;
    }

};

class VisitedListPool {

private:
    std::deque<VisitedList*> pool;
    std::mutex poolguard;
    size_t numelements;

public:
    VisitedListPool(size_t initmaxpools, size_t numelements) : numelements(numelements) {
        for(size_t i = 0; i < initmaxpools; i++) {
            pool.push_front(new VisitedList(numelements));
        }
    }

    VisitedList* getFreeVisitedList() {
        VisitedList* rez;
        {
            std::unique_lock<std::mutex> lock(poolguard);
            if(pool.size() > 0) {
                rez = pool.front();
                pool.pop_front();
            }
            else {
                rez = new VisitedList(numelements);
            }
        }
        rez->reset();
        return rez;
    }

    void releaseVisitedList(VisitedList* vl) {
        std::unique_lock<std::mutex> lock(poolguard);
        pool.push_front(vl);
    }

    ~VisitedListPool() {
        while(pool.size()) {
            VisitedList* rez = pool.front();
            pool.pop_front();
            delete rez;
        }
    }

};

}