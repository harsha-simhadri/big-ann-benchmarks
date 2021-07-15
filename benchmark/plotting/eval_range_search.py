"""
This script contains functions to evaluate the range search results.

Range search results are represented like a sparse CSR matrix with 3 components:

   lims, I, D

The results for query #q are:

   I[lims[q]:lims[q + 1]] in int

And the corresponding distances are:

   D[lims[q]:lims[q + 1]] in float

Thus, len(lims) = nq + 1, lims[i + 1] >= lims[i] forall i
and len(D) = len(I) = lims[-1].

The function that computes the Average Precision measure for
a search result vs. the ground-truth is compute_AP.

Note that the ground truth format in datasets.py is slightly different:
instead of lims it returns the number of results per query, nres.
The relationship between them is

   nres = lims[1:] - lims[:-1]

and

   lims = np.zeros(len(nres) + 1, int)
   lims[1:] = np.cumsum(nres)

"""

import numpy as np
from multiprocessing.pool import ThreadPool

## code copied from Faiss contrib

def counts_to_PR(ngt, nres, ninter, mode="overall"):
    """ computes a  precision-recall for a ser of queries.
    ngt = nb of GT results per query
    nres = nb of found results per query
    ninter = nb of correct results per query (smaller than nres of course)
    """

    if mode == "overall":
        ngt, nres, ninter = ngt.sum(), nres.sum(), ninter.sum()

        if nres > 0:
            precision = ninter / nres
        else:
            precision = 1.0

        if ngt > 0:
            recall = ninter / ngt
        elif nres == 0:
            recall = 1.0
        else:
            recall = 0.0

        return precision, recall

    elif mode == "average":
        # average precision and recall over queries

        mask = ngt == 0
        ngt[mask] = 1

        recalls = ninter / ngt
        recalls[mask] = (nres[mask] == 0).astype(float)

        # avoid division by 0
        mask = nres == 0
        assert np.all(ninter[mask] == 0)
        ninter[mask] = 1
        nres[mask] = 1

        precisions = ninter / nres

        return precisions.mean(), recalls.mean()

    else:
        raise AssertionError()


def sort_range_res_2(lims, D, I):
    """ sort 2 arrays using the first as key """
    I2 = np.empty_like(I)
    D2 = np.empty_like(D)
    nq = len(lims) - 1
    for i in range(nq):
        l0, l1 = lims[i], lims[i + 1]
        ii = I[l0:l1]
        di = D[l0:l1]
        o = di.argsort()
        I2[l0:l1] = ii[o]
        D2[l0:l1] = di[o]
    return I2, D2


def sort_range_res_1(lims, I):
    I2 = np.empty_like(I)
    nq = len(lims) - 1
    for i in range(nq):
        l0, l1 = lims[i], lims[i + 1]
        I2[l0:l1] = I[l0:l1]
        I2[l0:l1].sort()
    return I2


def range_PR_multiple_thresholds(
            lims_ref, Iref,
            lims_new, Dnew, Inew,
            thresholds,
            mode="overall", do_sort="ref,new"
    ):
    """ compute precision-recall values for range search results
    for several thresholds on the "new" results.
    This is to plot PR curves
    """
    # ref should be sorted by ids
    if "ref" in do_sort:
        Iref = sort_range_res_1(lims_ref, Iref)

    # new should be sorted by distances
    if "new" in do_sort:
        Inew, Dnew = sort_range_res_2(lims_new, Dnew, Inew)

    def ref_result_for(i):
        return Iref[lims_ref[i]:lims_ref[i + 1]]

    def new_result_for(i):
        l0, l1 = lims_new[i], lims_new[i + 1]
        return Inew[l0:l1], Dnew[l0:l1]

    nq = lims_ref.size - 1
    assert lims_new.size - 1 == nq

    nt = len(thresholds)
    counts = np.zeros((nq, nt, 3), dtype="int64")

    def compute_PR_for(q):
        gt_ids = ref_result_for(q)
        res_ids, res_dis = new_result_for(q)

        counts[q, :, 0] = len(gt_ids)

        if res_dis.size == 0:
            # the rest remains at 0
            return

        # which offsets we are interested in
        nres = np.searchsorted(res_dis, thresholds)
        counts[q, :, 1] = nres

        if gt_ids.size == 0:
            return

        # find number of TPs at each stage in the result list
        ii = np.searchsorted(gt_ids, res_ids)
        ii[ii == len(gt_ids)] = -1
        n_ok = np.cumsum(gt_ids[ii] == res_ids)

        # focus on threshold points
        n_ok = np.hstack(([0], n_ok))
        counts[q, :, 2] = n_ok[nres]

    pool = ThreadPool(20)
    pool.map(compute_PR_for, range(nq))
    # print(counts.transpose(2, 1, 0))

    precisions = np.zeros(nt)
    recalls = np.zeros(nt)
    for t in range(nt):
        p, r = counts_to_PR(
                counts[:, t, 0], counts[:, t, 1], counts[:, t, 2],
                mode=mode
        )
        precisions[t] = p
        recalls[t] = r

    return precisions, recalls



def compute_AP(gt, res):
    """
    compute range search average precision.
    It works by:
    1. defining a set of thresholds
    2. compute precision, recall for the thresholds
    3. compute AUC of rhe precision-recall curve.
    """
    gt_lims, gt_I, gt_D = gt
    res_lims, res_I, res_D = res

    if len(res_D) == 0:
        return 0.0

    # start with negative distance to be sure to have the
    # (p, r) = (1, 0) point
    dmax = res_D.max()
    thresholds = np.linspace(-0.001, res_D.max(), 100)

    precisions, recalls = range_PR_multiple_thresholds(
        gt_lims, gt_I,
        res_lims, res_D, res_I, thresholds)

    # compute average precision using trapezoids
    accu = 0
    n = len(precisions)
    for i in range(n - 1):
        x0, x1 = recalls[i : i + 2]
        y0, y1 = precisions[i : i + 2]
        accu += (x1 - x0) * (y1 + y0) / 2

    return accu


