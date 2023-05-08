
// -*- C++ -*-
%module bow_id_selector

/*
To compile:

# checkout of faiss
FAISS_SRC=$HOME/faiss_versions/faiss_latest_cmake

fields=( $( python -c 'import faiss, os; os.system("cat /proc/%d/maps" % os.getpid())' | grep libfaiss_avx2.so | head -1  ) )
LIBFAISS=${fields[5]}

swig -c++ -python -I$FAISS_SRC bow_id_selector.swig && \
   g++ -shared -O3 -g -fPIC bow_id_selector_wrap.cxx -o _bow_id_selector.so \
   -I $( python -c "import distutils.sysconfig ; print(distutils.sysconfig.get_python_inc())" ) \
   -I $FAISS_SRC \
   $LIBFAISS


*/


%{

#include <faiss/impl/FaissException.h>
#include <faiss/impl/IDSelector.h>

%}

#pragma SWIG nowarn=321
#pragma SWIG nowarn=403
#pragma SWIG nowarn=325
#pragma SWIG nowarn=389
#pragma SWIG nowarn=341
#pragma SWIG nowarn=512




%include <std_string.i>

typedef unsigned long size_t;
typedef unsigned int uint32_t;
typedef int int32_t;

namespace faiss {
using idx_t = long int;

}

%import(module="faiss") "faiss/MetricType.h"
%import(module="faiss") "faiss/impl/IDSelector.h"


// Python-specific: release GIL by default for all functions
%exception {
    Py_BEGIN_ALLOW_THREADS
    try {
        $action
    } catch(faiss::FaissException & e) {
        PyEval_RestoreThread(_save);

        if (PyErr_Occurred()) {
            // some previous code already set the error type.
        } else {
            PyErr_SetString(PyExc_RuntimeError, e.what());
        }
        SWIG_fail;
    } catch(std::bad_alloc & ba) {
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_MemoryError, "std::bad_alloc");
        SWIG_fail;
    }
    Py_END_ALLOW_THREADS
}



%inline %{

struct IDSelectorBOW : faiss::IDSelector {
    size_t nb;
    using TL = int32_t;
    const TL *lims;
    const int32_t *indices;
    int32_t w1 = -1, w2 = -1;

    IDSelectorBOW(
        size_t nb, const TL *lims, const int32_t *indices):
        nb(nb), lims(lims), indices(indices) {}

    void set_query_words(int32_t w1, int32_t w2) {
        this->w1 = w1;
        this->w2 = w2;
    }

    // binary search in the indices array
    bool find_sorted(TL l0, TL l1, int32_t w) const {
        while (l1 > l0 + 1) {
            TL lmed = (l0 + l1) / 2;
            if (indices[lmed] > w) {
                l1 = lmed;
            } else {
                l0 = lmed;
            }
        }
        return indices[l0] == w;
    }

    bool is_member(faiss::idx_t id) const {
        TL l0 = lims[id], l1 = lims[id + 1];
        if (l1 <= l0) {
            return false;
        }
        if(!find_sorted(l0, l1, w1)) {
            return false;
        }
        if(w2 >= 0 && !find_sorted(l0, l1, w2)) {
            return false;
        }
        return true;
    }

    ~IDSelectorBOW() override {}
};


struct IDSelectorBOWBin : IDSelectorBOW {
    /** with additional binary filtering */
    faiss::idx_t id_mask;

    IDSelectorBOWBin(
        size_t nb, const TL *lims, const int32_t *indices, faiss::idx_t id_mask):
        IDSelectorBOW(nb, lims, indices), id_mask(id_mask) {}

    faiss::idx_t q_mask = 0;

    void set_query_words_mask(int32_t w1, int32_t w2, faiss::idx_t q_mask) {
        set_query_words(w1, w2);
        this->q_mask = q_mask;
    }

    bool is_member(faiss::idx_t id) const {
        if ((id & id_mask) == 7037558) {
            printf("id=%ld id_mask=%ld q_mask=%ld\n", id, id_mask, q_mask);
        }
        if (q_mask & ~id) {
            return false;
        }
        return IDSelectorBOW::is_member(id & id_mask);
    }

    ~IDSelectorBOWBin() override {}
};


size_t intersect_sorted(
    size_t n1, const int32_t *a1,
    size_t n2, const int32_t *a2,
    int32_t *res)
{
    if (n1 == 0 || n2 == 0) {
        return 0;
    }
    size_t i1 = 0, i2 = 0, i = 0;
    for(;;) {
        if (a1[i1] < a2[i2]) {
            i1++;
            if (i1 >= n1) {
                return i;
            }
        } else if (a1[i1] > a2[i2]) {
            i2++;
            if (i2 >= n2) {
                return i;
            }
        } else { // equal
            res[i++] = a1[i1++];
            i2++;
            if (i1 >= n1 || i2 >= n2) {
                return i;
            }
        }
    }
}



%}


%pythoncode %{
# a few additional Python functions


%}