#pragma once

#ifndef NO_MANUAL_VECTORIZATION
#ifdef __SSE__
#define USE_SSE
#ifdef __AVX__
#define USE_AVX
#if defined(__AVX512F__) && defined(__AVX512DQ__)
#define USE_AVX512
#if defined(__AVX512VNNI__) && defined(__AVX512VL__) && defined(__AVX512BW__)
#define USE_AVX512_VNNI
#endif
#endif
#endif
#endif
#endif

#if defined(USE_AVX) || defined(USE_SSE)
#ifdef _MSC_VER
#include <intrin.h>
#include <stdexcept>
#else
#include <x86intrin.h>
#endif

#if defined(__GNUC__)
#define PORTABLE_ALIGN32 __attribute__((aligned(32)))
#else
#define PORTABLE_ALIGN32 __declspec(align(32))
#endif
#endif

#include <queue>

namespace hnswlib {

typedef size_t labeltype;

using VPFUNC = void (*)(void*, size_t);

template<typename Tdist>
using DISTFUNC = Tdist (*)(const void*, const void*, size_t);

template<typename Tdist>
class SpaceInterface {
private:
    size_t d;

public:
    SpaceInterface(size_t d) : d(d) {}

    virtual ~SpaceInterface() {}

    size_t getDim() const {
        return d;
    }

    virtual size_t getRawDataSize() const = 0;

    virtual inline size_t getDataSize() const {
        return getRawDataSize();
    }

    virtual inline VPFUNC getVectorPreprocessFunc() const {
        return nullptr;
    }

    virtual DISTFUNC<Tdist> getDistFunc() const = 0;

    virtual inline DISTFUNC<Tdist> getDistFuncST() const = 0;

};

class Level0StorageInterface {

public:
    virtual ~Level0StorageInterface() {}

    virtual void* allocate(size_t size) = 0;

    virtual void* load(FILE* file, size_t offset, size_t size) = 0;

    virtual void free(void* buf, size_t size) = 0;

};

template<typename Tdist>
class AlgorithmInterface {

public:
    virtual ~AlgorithmInterface() {}

    virtual void addPoint(const void* point, labeltype label) = 0;

    virtual std::priority_queue<std::pair<Tdist, labeltype>> searchKnn(const void* point, size_t topk) const = 0;

};

}

#include "bfp16.h"
#include "hnswalg.h"
#include "space_ip.h"
#include "space_l2.h"
#include "level0_storage.h"