
# Explanation of Optanne GraphANN Anomalies

From "sourabh.dongaonkar@intel.com":

Our implementation does not include a query response caching mechanism of any kind.

The anomalies, as defined, count the times the first query in the query set is slower than the last.

The reasons for this observation are:

- Julia is a "just-ahead-of-time" compiled language where the first call to a method triggers compilation of that method. Our heuristics for triggering the this compilation catch most of the required methods for our algorithm, but miss all of the function in the python binding library which still must be compiled when the first batch of queries is performed. Since overall execution time of the batch of queries is low, the relative overhead of this compilation is significant.

- Other overheads like initial allocations, and dynamic clock frequency ramp up would also tend to slow down the first query.
