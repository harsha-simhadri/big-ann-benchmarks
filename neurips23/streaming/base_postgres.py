import subprocess
import time
import numpy as np
import psycopg
import concurrent.futures

from math import ceil
from neurips23.streaming.base import BaseStreamingANN
from pgvector.psycopg import register_vector


PG_CONN_STR = "dbname=postgres user=postgres port=5432 host=localhost"


def cursor_print_and_execute(cur, query):
    print(query)
    cur.execute(query)

class BaseStreamingANNPostgres(BaseStreamingANN):
    # Child classes should implement the following methods ..:
    # - determine_index_op_class(self, metric)
    # - determine_query_op(self, metric)
    #
    # .. as well as setting the following attributes in their __init__ methods before calling super().__init__:
    # - self.name
    # - self.pg_index_method
    # - self.guc_prefix
    def determine_index_op_class(self, metric):
        raise NotImplementedError()

    def determine_query_op(self, metric):
        raise NotImplementedError()

    def __init__(self, metric, index_params):
        self.n_insert_conns = index_params.get("insert_conns")
        if self.n_insert_conns == None:
            raise Exception('Missing parameter insert_conns')

        # we'll initialize the connections later in set_query_arguments() per "query-arguments" set
        self.conns = []

        self.index_build_params = {k: v for k, v in index_params.items() if k != "insert_conns"}

        self.ind_op_class = self.determine_index_op_class(metric)
        self.query_op = self.determine_query_op(metric)

        start_database_result = subprocess.run(['bash', '/home/app/start_database.sh'], capture_output=True, text=True)
        if start_database_result.returncode != 0:
            raise Exception(f'Failed to start the database: {start_database_result.stderr}')

    def setup(self, dtype, max_pts, ndim):
        if dtype != 'float32':
            raise Exception('Invalid data type')

        index_build_params_clause = ""
        if self.index_build_params:
            index_build_params_clause = "WITH ("
            first = True
            for k, v in self.index_build_params.items():
                if not first:
                    index_build_params_clause += ", "

                first = False
                index_build_params_clause += f"{k} = {v}"

            index_build_params_clause += ")"

        # create the table and index by using a temporary connection
        with psycopg.connect(PG_CONN_STR, autocommit=True) as conn:
            with conn.cursor() as cur:
                cursor_print_and_execute(cur, f"CREATE TABLE test_tbl (id bigint, vec_col vector({ndim}))")
                cursor_print_and_execute(cur, f"CREATE INDEX vec_col_idx ON test_tbl USING {self.pg_index_method} (vec_col {self.ind_op_class}) {index_build_params_clause}")

        # required by insert() & delete()
        self.max_pts = max_pts
        self.active_indices = set()
        self.num_unprocessed_deletes = 0

        print('Index class constructed and ready')

    def done(self):
        # close any existing connections
        for conn in self.conns:
            conn.close()

        super().done()

    def insert(self, X, ids):
        n_insert_rows = len(ids)

        self.active_indices.update(ids+1)

        print('#active pts', len(self.active_indices), '#unprocessed deletes', self.num_unprocessed_deletes, '#inserting', n_insert_rows)

        # Execute VACUUM if the number of active points + the number of unprocessed deletes exceeds the max_pts
        if len(self.active_indices) + self.num_unprocessed_deletes >= self.max_pts:
            print('Executing VACUUM')

            start_time = time.time()

            with self.conns[0].cursor() as cur:
                cur.execute('VACUUM test_tbl')

            exec_time = time.time() - start_time

            log_dict = {
                'vacuum': self.num_unprocessed_deletes,
                'exec_time': exec_time
            }

            print('Timing:', log_dict)

            self.num_unprocessed_deletes = 0

        def copy_data(conn_idx, id_start_idx, id_end_idx):
            with self.conns[conn_idx].cursor().copy("COPY test_tbl (id, vec_col) FROM STDIN") as copy:
                for id, vec in zip(ids[id_start_idx:id_end_idx], X[id_start_idx:id_end_idx]):
                    copy.write_row((id, vec))

        # Run the copy_data function in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_insert_conns) as executor:
            chunk_size = ceil(n_insert_rows / self.n_insert_conns)
            copy_futures = []
            for conn_idx, id_start_idx in enumerate(range(0, n_insert_rows, chunk_size)):
                id_end_idx = min(id_start_idx + chunk_size, n_insert_rows)
                copy_futures.append(executor.submit(copy_data, conn_idx, id_start_idx, id_end_idx))

            start_time = time.time()

            for copy_future in concurrent.futures.as_completed(copy_futures):
                # raise any exceptions that occurred during execution
                copy_future.result()

            exec_time = time.time() - start_time

            log_dict = {
                'insert': n_insert_rows,
                'exec_time': exec_time
            }

            print('Timing:', log_dict)

    def delete(self, ids):
        n_delete_rows = len(ids)

        start_time = time.time()

        with self.conns[0].cursor() as cur:
            # delete ids in batches of 1000
            for i in range(0, n_delete_rows, 1000):
                subset = [x for x in ids[i:i+1000]]
                cur.execute("DELETE FROM test_tbl WHERE id = ANY(%s)", (subset,))

        exec_time = time.time() - start_time

        log_dict = {
            'delete': n_delete_rows,
            'exec_time': exec_time
        }

        print('Timing:', log_dict)

        self.active_indices.difference_update(ids+1)
        self.num_unprocessed_deletes += n_delete_rows

    def query(self, X, k):
        def batch_query(conn_idx, query_vec_start_idx, query_vec_end_idx):
            batch_result_id_lists = []
            for query_vec in X[query_vec_start_idx: query_vec_end_idx]:
                with self.conns[conn_idx].cursor() as cur:
                    try:
                        cur.execute(f"SELECT id FROM test_tbl ORDER BY vec_col {self.query_op} %s LIMIT {k}", (query_vec, ))
                    except Exception as e:
                        raise Exception(f"Error '{e}' when querying with k={k}\nQuery vector was:\n{query_vec}") from e

                    result_tuples = cur.fetchall()

                    result_ids = list(map(lambda tup: tup[0], result_tuples))

                    if len(result_ids) < k:
                        # Pad with -1 if we have less than k results. This is only needed if the
                        # index-access method cannot guarantee returning k results.
                        #
                        # As of today, this is only possible with PostgresPgvectorHnsw when
                        # ef_search < k.
                        result_ids.extend([-1] * (k - len(result_ids)))

                    batch_result_id_lists.append(result_ids)

            return batch_result_id_lists

        total_queries = len(X)

        result_id_lists = []

        # Run the batch_query function in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_query_conns) as executor:
            chunk_size = ceil(total_queries / self.n_query_conns)
            query_futures = []
            for conn_idx, query_vec_start_idx in enumerate(range(0, total_queries, chunk_size)):
                query_vec_end_idx = min(query_vec_start_idx + chunk_size, total_queries)
                query_futures.append(executor.submit(batch_query, conn_idx, query_vec_start_idx, query_vec_end_idx))

            start_time = time.time()

            # wait for all futures to complete
            done, not_done = concurrent.futures.wait(query_futures)

            exec_time = time.time() - start_time

            log_dict = {
                'query': total_queries,
                'exec_time': exec_time
            }

            print('Timing:', log_dict)

            assert len(not_done) == 0
            assert len(done) == len(query_futures)

            # retrieve the results in the order they were submitted to avoid messing up the order
            for query_future in query_futures:
                batch_result_id_lists = query_future.result()
                result_id_lists.extend(batch_result_id_lists)

        self.res = np.vstack(result_id_lists, dtype=np.int32)

    def set_query_arguments(self, query_args):
        # close any existing connections
        for conn in self.conns:
            conn.close()

        # By using a temporary connection, truncate the table since set_query_arguments() is called
        # before each testing phase with new set of query params.
        with psycopg.connect(PG_CONN_STR, autocommit=True) as conn:
            with conn.cursor() as cur:
                cursor_print_and_execute(cur, "TRUNCATE test_tbl")

        self.n_query_conns = query_args.get("query_conns")
        if self.n_query_conns == None:
            raise Exception('Missing parameter query_conns')

        n_conns_needed = max(self.n_query_conns, self.n_insert_conns)

        self.conns = [psycopg.connect(PG_CONN_STR, autocommit=True) for _ in range(n_conns_needed)]

        # so that we can insert np arrays as pgvector's vector data type transparently
        for conn in self.conns:
            register_vector(conn)

        guc_args = {k: v for k, v in query_args.items() if k != "query_conns"}

        for conn in self.conns:
            with conn.cursor() as cur:
                for k, v in guc_args.items():
                    cursor_print_and_execute(cur, f"SET {self.guc_prefix}.{k} TO {v}")

                # disable seqscan for all connections since we mainly want to test index-scan
                cursor_print_and_execute(cur, f"SET enable_seqscan TO OFF")

    def __str__(self):
        return self.name
