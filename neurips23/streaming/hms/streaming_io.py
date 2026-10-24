"""Read only the requested source rows, without a whole-source memory mapping."""
import operator
import os
import struct

import numpy as np

from benchmark.datasets import MSTuringClustered10M, MSTuringClustered30M


def read_fbin_range(filename, start, end, rows, dim):
    start, end, rows, dim = map(operator.index, (start, end, rows, dim))
    if rows < 0 or dim <= 0 or not 0 <= start <= end <= rows:
        raise ValueError("invalid source row range or dimensions")
    count = (end - start) * dim
    if count > np.iinfo(np.intp).max // 4:
        raise ValueError("source range allocation is too large")
    with open(filename, "rb") as source:
        if source.read(8) != struct.pack("<II", rows, dim):
            raise ValueError("source dimensions do not match the dataset")
        if os.fstat(source.fileno()).st_size != 8 + rows * dim * 4:
            raise ValueError("source length does not match its dimensions")
        source.seek(8 + start * dim * 4)
        values = np.fromfile(source, dtype="<f4", count=count)
    if values.size != count:
        raise ValueError("source was truncated while reading")
    return values.reshape(end - start, dim)


class _RangeReader:
    def get_data_in_range(self, start, end):
        return read_fbin_range(self.get_dataset_fn(), start, end, self.nb, self.d)

    def short_name(self):
        return f"{self.dataset_type.__name__}-{self.nb}"


class MSTuring10MRangeReader(_RangeReader, MSTuringClustered10M):
    dataset_type = MSTuringClustered10M


class MSTuring30MRangeReader(_RangeReader, MSTuringClustered30M):
    dataset_type = MSTuringClustered30M
