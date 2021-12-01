
# Explanation of Optanne GraphANN Anomalies

From "sourabh.dongaonkar@intel.com":

"We think that this is primarily because Julia is a just-in-time (JIT) compiled language.

So the first time the search function is called, it triggers a compilation, and is slower.

We can fix this by triggering pre-compilation in the load step, which will be a couple of lines of code change.

We will also be happy to have the code examined by the organizers if needed.

Please let me know if you would like us to put in this fix."
