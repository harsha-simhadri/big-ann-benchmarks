#pragma once

#include "bfp16.h"

#include <x86intrin.h>

template <typename Tdist, typename Tcorr>
static Tdist L2SqrRef(const Tcorr* a, const Tcorr* b, size_t d) {
    Tdist sum = 0;
    for(size_t i = 0; i < d; i++) {
        Tdist diff = Tdist(a[i]) - Tdist(b[i]);
        sum += diff * diff;
    }
    return sum;
}

static float L2Sqr(const float* a, const float* b, size_t d) {
#ifdef USE_SSE
#ifdef USE_AVX
#ifdef USE_AVX512
    __m512 msum512 = _mm512_setzero_ps();
    while(d >= 16) {
        __m512 ma = _mm512_loadu_ps(a);
        a += 16;
        __m512 mb = _mm512_loadu_ps(b);
        b += 16;
        __m512 mdiff = _mm512_sub_ps(ma, mb);
        msum512 = _mm512_add_ps(msum512, _mm512_mul_ps(mdiff, mdiff));
        d -= 16;
    }
    if(d == 0) {
        return _mm512_reduce_add_ps(msum512);
    }
    __m256 msum256 = _mm512_extractf32x8_ps(msum512, 1);
    msum256 = _mm256_add_ps(msum256, _mm512_extractf32x8_ps(msum512, 0));
    if(d >= 8) {
#else
    __m256 msum256 = _mm256_setzero_ps();
    while(d >= 8) {
#endif
        __m256 ma = _mm256_loadu_ps(a);
        a += 8;
        __m256 mb = _mm256_loadu_ps(b);
        b += 8;
        __m256 mdiff = _mm256_sub_ps(ma, mb);
        msum256 = _mm256_add_ps(msum256, _mm256_mul_ps(mdiff, mdiff));
        d -= 8;
    }
    __m128 msum128 = _mm256_extractf128_ps(msum256, 1);
    msum128 = _mm_add_ps(msum128, _mm256_extractf128_ps(msum256, 0));
    if(d >= 4) {
#else
    __m128 msum128 = _mm_setzero_ps();
    while(d >= 4) {
#endif
        __m128 ma = _mm_loadu_ps(a);
        a += 4;
        __m128 mb = _mm_loadu_ps(b);
        b += 4;
        __m128 mdiff = _mm_sub_ps(ma, mb);
        msum128 = _mm_add_ps(msum128, _mm_mul_ps(mdiff, mdiff));
        d -= 4;
    }
    msum128 = _mm_hadd_ps(msum128, msum128);
    msum128 = _mm_hadd_ps(msum128, msum128);
    float sum = _mm_cvtss_f32(msum128);
    return d ? sum + L2SqrRef<float, float>(a, b, d) : sum;
#else
    return L2SqrRef<float, float>(a, b, d);
#endif
}

static float L2Sqr(const bfp16_t* a, const bfp16_t* b, size_t d) {
#ifdef USE_SSE
#ifdef USE_AVX
#ifdef USE_AVX512
    __m512 msum512 = _mm512_setzero_ps();
    while(d >= 16) {
        __m512 ma = _mm512_castsi512_ps(_mm512_slli_epi32(_mm512_cvtepi16_epi32(
                _mm256_loadu_si256((const __m256i_u*)a)), 16));
        a += 16;
        __m512 mb = _mm512_castsi512_ps(_mm512_slli_epi32(_mm512_cvtepi16_epi32(
                _mm256_loadu_si256((const __m256i_u*)b)), 16));
        b += 16;
        __m512 mdiff = _mm512_sub_ps(ma, mb);
        msum512 = _mm512_add_ps(msum512, _mm512_mul_ps(mdiff, mdiff));
        d -= 16;
    }
    if(d == 0) {
        return _mm512_reduce_add_ps(msum512);
    }
    __m256 msum256 = _mm512_extractf32x8_ps(msum512, 1);
    msum256 = _mm256_add_ps(msum256, _mm512_extractf32x8_ps(msum512, 0));
    if(d >= 8) {
#else
    __m256 msum256 = _mm256_setzero_ps();
    while(d >= 8) {
#endif
        __m256 ma = _mm256_castsi256_ps(_mm256_slli_epi32(_mm256_cvtepi16_epi32(
                _mm_loadu_si128((const __m128i_u*)a)), 16));
        a += 8;
        __m256 mb = _mm256_castsi256_ps(_mm256_slli_epi32(_mm256_cvtepi16_epi32(
                _mm_loadu_si128((const __m128i_u*)b)), 16));
        b += 8;
        __m256 mdiff = _mm256_sub_ps(ma, mb);
        msum256 = _mm256_add_ps(msum256, _mm256_mul_ps(mdiff, mdiff));
        d -= 8;
    }
    __m128 msum128 = _mm256_extractf128_ps(msum256, 1);
    msum128 = _mm_add_ps(msum128, _mm256_extractf128_ps(msum256, 0));
    if(d >= 4) {
#else
    __m128 msum128 = _mm_setzero_ps();
    while(d >= 4) {
#endif
        __m128 ma = _mm_castsi128_ps(_mm_slli_epi32(_mm_cvtepi16_epi32(
                _mm_loadl_epi64((const __m128i_u*)a)), 16));
        a += 4;
        __m128 mb = _mm_castsi128_ps(_mm_slli_epi32(_mm_cvtepi16_epi32(
                _mm_loadl_epi64((const __m128i_u*)b)), 16));
        b += 4;
        __m128 mdiff = _mm_sub_ps(ma, mb);
        msum128 = _mm_add_ps(msum128, _mm_mul_ps(mdiff, mdiff));
        d -= 4;
    }
    msum128 = _mm_hadd_ps(msum128, msum128);
    msum128 = _mm_hadd_ps(msum128, msum128);
    float sum = _mm_cvtss_f32(msum128);
    return d ? sum + L2SqrRef<float, bfp16_t>(a, b, d) : sum;
#else
    return L2SqrRef<float, bfp16_t>(a, b, d);
#endif
}

static int64_t L2Sqr(const int16_t* a, const int16_t* b, size_t d) {
#ifdef USE_SSE
#ifdef USE_AVX
#ifdef USE_AVX512
    __m512i msum512 = _mm512_setzero_si512();
    while(d >= 16) {
        __m512i ma = _mm512_cvtepi16_epi32(_mm256_loadu_si256((const __m256i_u*)a));
        a += 16;
        __m512i mb = _mm512_cvtepi16_epi32(_mm256_loadu_si256((const __m256i_u*)b));
        b += 16;
        __m512i mdiff = _mm512_sub_epi32(ma, mb);
        msum512 = _mm512_add_epi32(msum512, _mm512_mullo_epi32(mdiff, mdiff));
        d -= 16;
    }
    msum512 = _mm512_add_epi64(
            _mm512_cvtepi32_epi64(_mm512_extracti32x8_epi32(msum512, 1)),
            _mm512_cvtepi32_epi64(_mm512_extracti32x8_epi32(msum512, 0)));
    if(d == 0) {
        return _mm512_reduce_add_epi64(msum512);
    }
    __m256i msum256 = _mm512_extracti64x4_epi64(msum512, 1);
    msum256 = _mm256_add_epi64(msum256, _mm512_extracti64x4_epi64(msum512, 0));
    if(d >= 8) {
#else
    __m256i msum256 = _mm256_setzero_si256();
    while(d >= 8) {
#endif
        __m256i ma = _mm256_cvtepi16_epi32(_mm_loadu_si128((const __m128i_u*)a));
        a += 8;
        __m256i mb = _mm256_cvtepi16_epi32(_mm_loadu_si128((const __m128i_u*)b));
        b += 8;
        __m256i mmul = _mm256_sub_epi32(ma, mb);
        mmul = _mm256_mullo_epi32(mmul, mmul);
        msum256= _mm256_add_epi64(msum256, _mm256_cvtepi32_epi64(
                _mm_add_epi32(_mm256_extracti128_si256(mmul, 1), _mm256_extracti128_si256(mmul, 0))));
        d -= 8;
    }
    __m128i msum128 = _mm256_extracti128_si256(msum256, 1);
    msum128 = _mm_add_epi64(msum128, _mm256_extracti128_si256(msum256, 0));
    if(d >= 4) {
#else
    __m128i msum128 = _mm_setzero_si128();
    while(d >= 4) {
#endif
        __m128i ma = _mm_cvtepi16_epi32(_mm_loadl_epi64((const __m128i_u*)a));
        a += 4;
        __m128i mb = _mm_cvtepi16_epi32(_mm_loadl_epi64((const __m128i_u*)b));
        b += 4;
        __m128i mmul = _mm_sub_epi32(ma, mb);
        mmul = _mm_mullo_epi32(mmul, mmul);
        msum128 = _mm_add_epi64(msum128, _mm_cvtepi32_epi64(_mm_hadd_epi32(mmul, mmul)));
        d -= 4;
    }
    int64_t sum = _mm_extract_epi64(msum128, 1) + _mm_extract_epi64(msum128, 0);
    return d ? sum + InnerProductRef<int64_t, int16_t>(a, b, d) : sum;
#else
    return L2SqrRef<int64_t, int16_t>(a, b, d);
#endif
}

static int L2Sqr(const int8_t* a, const int8_t* b, size_t d) {
#ifdef USE_SSE
#ifdef USE_AVX
#ifdef USE_AVX512
    __m512i msum512 = _mm512_setzero_si512();
    while(d >= 16) {
        __m512i ma = _mm512_cvtepi8_epi32(_mm_loadu_si128((const __m128i_u*)a));
        a += 16;
        __m512i mb = _mm512_cvtepi8_epi32(_mm_loadu_si128((const __m128i_u*)b));
        b += 16;
        __m512i mdiff = _mm512_sub_epi32(ma, mb);
        msum512 = _mm512_add_epi32(msum512, _mm512_mullo_epi32(mdiff, mdiff));
        d -= 16;
    }
    if(d == 0) {
        return _mm512_reduce_add_epi32(msum512);
    }
    __m256i msum256 = _mm512_extracti32x8_epi32(msum512, 1);
    msum256 = _mm256_add_epi32(msum256, _mm512_extracti32x8_epi32(msum512, 0));
    if(d >= 8) {
#else
    __m256i msum256 = _mm256_setzero_si256();
    while(d >= 8) {
#endif
        __m256i ma = _mm256_cvtepi8_epi32(_mm_loadl_epi64((const __m128i_u*)a));
        a += 8;
        __m256i mb = _mm256_cvtepi8_epi32(_mm_loadl_epi64((const __m128i_u*)b));
        b += 8;
        __m256i mdiff = _mm256_sub_epi32(ma, mb);
        msum256 = _mm256_add_epi32(msum256, _mm256_mullo_epi32(mdiff, mdiff));
        d -= 8;
    }
    __m128i msum128 = _mm256_extracti128_si256(msum256, 1);
    msum128 = _mm_add_epi32(msum128, _mm256_extracti128_si256(msum256, 0));
    if(d >= 4) {
#else
    __m128i msum128 = _mm_setzero_si128();
    while(d >= 4) {
#endif
        __m128i ma = _mm_cvtepi8_epi32(_mm_castps_si128(_mm_load1_ps((const float*)a)));
        a += 4;
        __m128i mb = _mm_cvtepi8_epi32(_mm_castps_si128(_mm_load1_ps((const float*)b)));
        b += 4;
        __m128i mdiff = _mm_sub_epi32(ma, mb);
        msum128 = _mm_add_epi32(msum128, _mm_mullo_epi32(mdiff, mdiff));
        d -= 4;
    }
    msum128 = _mm_hadd_epi32(msum128, msum128);
    msum128 = _mm_hadd_epi32(msum128, msum128);
    int sum = _mm_cvtsi128_si32(msum128);
    return d ? sum + L2SqrRef<int, int8_t>(a, b, d) : sum;
#else
    return L2SqrRef<int, int8_t>(a, b, d);
#endif
}

static inline float L2SqrST(const float* x, const float* y, size_t d) {
    return L2Sqr(x, y, d);
}

static inline float L2SqrST(const bfp16_t* x, const bfp16_t* y, size_t d) {
    return L2Sqr(x, y, d);
}

static inline int64_t L2SqrST(const int16_t* x, const int16_t* y, size_t d) {
    return L2Sqr(x, y, d);
}

static inline int L2SqrST(const int8_t* x, const int8_t* y, size_t d) {
    return L2Sqr(x, y, d);
}
