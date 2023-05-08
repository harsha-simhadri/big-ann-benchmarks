
%module bow_id_selector

/*
To compile when Faiss is installed via conda:

swig -c++ -python -I$CONDA_PREFIX/include  bow_id_selector.swig &&  \
g++ -shared -O3 -g -fPIC bow_id_selector_wrap.cxx -o _bow_id_selector.so  \
  -I $( python -c "import distutils.sysconfig ; print(distutils.sysconfig.get_python_inc())" )  \
  -I $CONDA_PREFIX/include $CONDA_PREFIX/lib/libfaiss_avx2.so

*/


// Put C++ includes here
%{

#include <faiss/impl/FaissException.h>
#include <faiss/impl/IDSelector.h>

%}

// to get uint32_t and friends
%include <stdint.i>

// This means: assume what's declared in these .h files is provided
// by the Faiss module.
%import(module="faiss") "faiss/MetricType.h"
%import(module="faiss") "faiss/impl/IDSelector.h"

// functions to be parsed here

// This is important to release GIL and do Faiss exception handing
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


// any class or function declared below will be made available
// in the module.
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
        if (q_mask & ~id) {
            return false;
        }
        return IDSelectorBOW::is_member(id & id_mask);
    }

    ~IDSelectorBOWBin() override {}
};


size_t intersect_sorted_c(
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

import numpy as np

# example additional function that converts the passed-in numpy arrays to
# C++ pointers
def intersect_sorted(a1, a2):
    n1, = a1.shape
    n2, = a2.shape
    res = np.empty(n1 + n2, dtype=a1.dtype)
    nres = intersect_sorted_c(
        n1, faiss.swig_ptr(a1),
        n2, faiss.swig_ptr(a2),
        faiss.swig_ptr(res)
    )
    return res[:nres]

%}