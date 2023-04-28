
// -*- C++ -*-
%module bow_id_selector

/*
To compile:

# checkout of faiss
FAISS_SRC=$HOME/faiss_versions/faiss_latest_cmake

fields=( $( python -c 'import faiss, os; os.system("cat /proc/%d/maps" % os.getpid())' | grep libfaiss_avx2.so | head -1  ) )
LIBFAISS=${fields[5]}

swig -c++ -python -I$FAISS_SRC bow_id_selector.swig && \
   g++ -shared -fPIC bow_id_selector_wrap.cxx -o _bow_id_selector.so \
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


    bool is_member(faiss::idx_t id) const final {
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

%}


%pythoncode %{
# a few additional Python functions


%}