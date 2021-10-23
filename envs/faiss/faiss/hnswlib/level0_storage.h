#pragma once

#include "hnswlib.h"

#include <sys/mman.h>

namespace hnswlib {

class VmemLevel0 : public Level0StorageInterface {

public:
    void* allocate(size_t size) override {
        void* buf = malloc(size);
        if(buf == nullptr) {
            throw std::runtime_error("out of memory");
        }
        return buf;
    }

    void* load(FILE* file, size_t offset, size_t size) override {
        char* buf = (char*)malloc(size);
        if(buf == nullptr) {
            throw std::runtime_error("Not enough memory: loadIndex failed to allocate level0");
        }
        if(fseek(file, offset, SEEK_SET) < 0) {
            throw std::runtime_error("failed to set current position of file");
        }
        if(fread(buf, 1, size, file) != size) {
            throw std::runtime_error("failed to read from file");
        }
        return buf;
    }

    void free(void* buf, size_t /*size*/) override {
        ::free(buf);
    }

};

class PmemLevel0 : public Level0StorageInterface {

public:
    void* allocate(size_t /*size*/) override {
        throw std::runtime_error("pmem is read only");
    }

    void* load(FILE* file, size_t offset, size_t size) override {
        int fd = fileno(file);
        if(fd < 0) {
            throw std::runtime_error("failed to get file descriptor of FILE");
        }
        void* buf = mmap(nullptr, size, PROT_READ, MAP_SHARED, fd, offset);
        if(buf == MAP_FAILED) {
            throw std::runtime_error(std::string("failed to mmap level0: ").append(strerror(errno)));
        }
        return buf;
    }

    void free(void* buf, size_t size) override {
        munmap(buf, size);
    }

};

}