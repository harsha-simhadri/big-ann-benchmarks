#pragma once

#include <stdint.h>

class Bfp16 {

private:
    union {
        uint16_t u16;
        struct {
            uint16_t mantissa : 7;
            uint16_t exponent : 8;
            uint16_t sign : 1;
        };
    }
    storage;

    typedef union {
        float value;
        struct {
            uint32_t mantissa : 23;
            uint32_t exponent : 8;
            uint32_t sign : 1;
        };
        uint16_t u16s[2];
    }
    Fp32Format;

public:
    inline Bfp16() {
    }

    template <typename T>
    inline Bfp16(const T& x) {
        *this = x;
    }

    template <typename T>
    inline void operator =(const T& x) {
        Fp32Format fp32;
        fp32.value = float(x);
        if(fp32.u16s[0] & 0x8000) {
            fp32.u16s[0] = 0;
            fp32.value *= 129.0f / 128.0f;
        }
        storage.u16 = fp32.u16s[1];
    }

    template <typename T>
    inline operator T() const {
        Fp32Format fp32;
        fp32.u16s[0] = 0;
        fp32.u16s[1] = storage.u16;
        return T(fp32.value);
    }

};

typedef Bfp16 bfp16_t;