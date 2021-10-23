#pragma once

#include "hnswlib.h"
#include "distance_ip.h"

namespace hnswlib {

template <typename Tdist, typename Tcorr>
static Tdist InnerProductDistFunc(const void* a, const void* b, size_t d) {
    return - InnerProduct((const Tcorr*)a, (const Tcorr*)b, d);
}

template <typename Tdist, typename Tcorr>
static Tdist InnerProductDistFuncST(const void* x, const void* y, size_t d) {
    return - InnerProductST((const Tcorr*)x, (const Tcorr*)y, d);
}

template <typename Tdist, typename Tcorr>
class InnerProductSpace : public SpaceInterface<Tdist> {

private:
    size_t raw_data_size_;

public:
    InnerProductSpace(size_t d): SpaceInterface<Tdist>(d) {
        raw_data_size_ = d * sizeof(Tcorr);
    }

    size_t getRawDataSize() const override {
        return raw_data_size_;
    }

    DISTFUNC<Tdist> getDistFunc() const override {
        return InnerProductDistFunc<Tdist, Tcorr>;
    }

    DISTFUNC<Tdist> getDistFuncST() const override {
        return InnerProductDistFuncST<Tdist, Tcorr>;
    }

    ~InnerProductSpace() {}

};

}
