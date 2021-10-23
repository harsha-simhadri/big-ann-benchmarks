#pragma once

#include "hnswlib.h"
#include "distance_l2.h"

#define OPT_HNSWLIB_L2EXP

#ifdef OPT_HNSWLIB_L2EXP
#include "distance_ip.h"
#endif

namespace hnswlib {

template <typename Tdist, typename Tcorr>
static Tdist L2SqrDistFunc(const void* a, const void* b, size_t d) {
    return L2Sqr((const Tcorr*)a, (const Tcorr*)b, d);
}

#ifndef OPT_HNSWLIB_L2EXP
template <typename Tdist, typename Tcorr>
static Tdist L2SqrDistFuncST(const void* x, const void* y, size_t d) {
    return L2SqrST((const Tcorr*)x, (const Tcorr*)y, d);
}
#else
template <typename Tdist, typename Tcorr>
static void L2expPreprocessFunc(void* y, size_t d) {
    const Tcorr* ty = (const Tcorr*)y;
    Tdist norm = 0;
    for(size_t i = 0; i < d; i++) {
        norm += Tdist(ty[i]) * Tdist(ty[i]);
    }
    Tdist* norm_ptr = (Tdist*)(size_t(y) + d * sizeof(Tcorr));
    *norm_ptr = norm;
}

template <typename Tdist, typename Tcorr>
static Tdist L2expDistFuncST(const void* x, const void* y, size_t d) {
    const Tdist* norm_ptr = (const Tdist*)(size_t(y) + d * sizeof(Tcorr));
    return -2 * InnerProductST((const Tcorr*)x, (const Tcorr*)y, d) + *norm_ptr;
}
#endif

template <typename Tdist, typename Tcorr>
class L2Space : public SpaceInterface<Tdist> {

private:
    size_t raw_data_size_;

public:
    L2Space(size_t dim): SpaceInterface<Tdist>(dim) {
        raw_data_size_ = dim * sizeof(Tcorr);
    }

    size_t getRawDataSize() const override {
        return raw_data_size_;
    }

    DISTFUNC<Tdist> getDistFunc() const override {
        return L2SqrDistFunc<Tdist, Tcorr>;
    }

#ifndef OPT_HNSWLIB_L2EXP
    DISTFUNC<Tdist> getDistFuncST() const override {
        return L2SqrDistFuncST<Tdist, Tcorr>;
    }
#else
    size_t getDataSize() const override {
        return raw_data_size_ + sizeof(Tdist);
    }

    VPFUNC getVectorPreprocessFunc() const override {
        return L2expPreprocessFunc<Tdist, Tcorr>;
    }

    DISTFUNC<Tdist> getDistFuncST() const override {
        return L2expDistFuncST<Tdist, Tcorr>;
    }
#endif

    ~L2Space() {}
};

}