import psycopg
import numpy as np
from pgvector.psycopg import register_vector

from neurips23.streaming.base import BaseStreamingANN

DISTANCE_METRICS = {
    "euclidean": "vector_l2_ops",
    "angular": "vector_cosine_ops",
    "ip": "vector_ip_ops",
}
TYPE_MAP = {
    "float32": "vector",
    "float16": "halfvec",
}


class RabbitHole(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.name = "rabbithole"
        self.nlist = index_params.get("nlist")
        self.metric = DISTANCE_METRICS.get(metric)
        self.conn = psycopg.connect("postgresql://postgres:postgres@127.0.0.1:5432/")
        self.conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        self.conn.execute("CREATE EXTENSION IF NOT EXISTS rabbithole")
        register_vector(self.conn)

    def setup(self, dtype, max_pts, ndims) -> None:
        self.dtype = TYPE_MAP.get(dtype, "vector")
        self.max_vectors = max_pts
        self.ndims = ndims
        self.config = f"""
residual_quantization = {'true' if self.metric == 'vector_l2_ops' else 'false'}
[build.internal]
lists = {self.nlist}
spherical_centroids = {'true' if self.metric != 'vector_l2_ops' else 'false'}
"""
        self.conn.execute(
            f"CREATE TABLE IF NOT EXISTS ann (id SERIAL PRIMARY KEY, emb {self.dtype}({self.ndims}))"
        )
        self.conn.execute(
            f"CREATE INDEX ON ann USING rabbithole (emb {self.metric}) WITH (options=$${self.config}$$)"
        )

    def set_query_arguments(self, query_args):
        self.query_args = query_args
        self.probe = query_args.get("probe")
        if self.probe:
            self.conn.execute(f"SET rabbithole.probes = {self.probe}")

    def insert(self, X, ids):
        with self.conn.cursor().copy(
            "COPY ann (id, emb) FROM STDIN WITH (FORMAT BINARY)"
        ) as copy:
            copy.set_types(("integer", "vector"))
            for i, vec in zip(ids, X):
                copy.write_row((i, vec))

    def delete(self, ids):
        self.conn.execute("DELETE FROM ann WHERE id = ANY(%s)", (list(ids),))

    def replace(self, dataset):
        return super().fit(dataset)

    def query(self, X, k):
        n = len(X)
        self.res = np.empty((n, k), dtype="uint32")
        for i, x in enumerate(X):
            rows = self.conn.execute(
                "SELECT id FROM ann ORDER BY emb <-> %s LIMIT %s", (x, k)
            ).fetchall()
            for j, (id,) in enumerate(rows):
                self.res[i, j] = id

    def range_query(self, X, radius):
        raise NotImplementedError

    def __str__(self):
        return f"RabbitHole(nlist={self.nlist},dim={self.ndims},type={self.dtype})"
