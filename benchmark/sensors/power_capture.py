import requests
import uuid
import json
import time
import statistics
import math

class power_capture:

    """
    This singleton class provides various capabilites related to the T3 track
    of the Big ANN Competition for NeurIPS 2021:
        * communicates with an ipmicap server ( see http://github.com/fractalsproject/ipmicap )
        * leverage's servers power sensor capture abilities
        * retrieves power statistics computed by the server
    """
    
    ipmicap_ip          = None
    ipmicap_port        = None
    min_capture_time    = None
    raise_exc_on_fail   = None

    @classmethod
    def __init__(cls, packed_parm, raise_exc_on_fail=True):
        
        parms = packed_parm.split(":")
        ipmicap_ip = parms[0]
        ipmicap_port = int(parms[1])
        min_capture_time = float(parms[2])
        cls.ipmicap_ip = ipmicap_ip
        cls.ipmicap_port = ipmicap_port
        cls.min_capture_time = min_capture_time
        cls.raise_exc_on_fail = raise_exc_on_fail

    @classmethod
    def _send_msg_to_ipmicap_server(cls, uri, parms):
        url = "http://%s:%d/%s" % (cls.ipmicap_ip,cls.ipmicap_port,uri)
        resp = requests.get(url,parms)
        if resp.status_code!=200:
            msg = "T3: Failed to ping ipmicapserver."
            if cls.raise_exc_on_fail: 
                raise Exception(msg)
            else: 
                print("Power: Failed to ping ipmicap server.")
                return False
        else: 
            ret_json = resp.json()
            return resp.json()
    
    @classmethod
    def enabled(cls):
        """
        Returns True if this singleton class has been initialized.
        """
        if cls.ipmicap_ip != None:
            return True
        else:
            return False

    @classmethod
    def ping(cls):
        """
        Ping the IPMICAP server and make sure it's running.
        """
        return cls._send_msg_to_ipmicap_server("log",{"ping":1})

    @classmethod
    def start(cls): 
        """
        Start power capture at the IPMI server.
        """
        session_id = str(uuid.uuid4())
        status = cls._send_msg_to_ipmicap_server("session",
            {"start":1,"id":session_id})
        if status:
            return session_id
        else:
            return False

    @classmethod
    def stop(cls, session_id, all_stats=False):
        """
        End power capture at the IPMI server for the session
        and returm the computed power consumption.
        """
        stop_parm = "all_stats" if all_stats else 1
        power_stats =  cls._send_msg_to_ipmicap_server("session",
            {"stop":stop_parm, "id": session_id})
        if power_stats:
            return power_stats
        else:
            return False

    @classmethod
    def get_stats(cls, session_ids):
        """
        Retrieve power capture statistics for capture ids supplied.
        """
        raise Exception("Not implemented.") 

    @classmethod
    def run_has_power_stats(cls, properties):
        """
        Determines if the benchmark run has power related metrics.
        """
        if "power_consumption" in properties: return True
        else: return False

    @classmethod
    def detect_power_benchmarks(cls, metrics, res):
        """
        Adjust the global metrics based on the availability of
        power related benchmarks in the loaded results.  
        """
        has_power_benchmarks = False
        for i, (properties, run) in enumerate(res):
            if cls.run_has_power_stats(properties):
                has_power_benchmarks = True
                break
        if has_power_benchmarks: 
            return True
        else: # no power benchmarks and not required, just remove from global benchmarks
            #print("Ignoring the global 'wspq' metric because no power benchmarks are present.")
            metrics.pop("wspq", None)
            return True

    @classmethod
    def detect_power_benchmarks_for_plot(cls, args, res ):
        """
        If power benchmarks are requested for plot but now power benchmarks are
        not present then return False.
        """
        required = args.x_axis=='wspq'  or args.y_axis=='wspq'
        if not required:
            return True

        has_power_benchmarks = False
        for i, (properties, run) in enumerate(res):
            if cls.run_has_power_stats(properties):
                has_power_benchmarks = True
                break
        if has_power_benchmarks and required: return True
        else: 
            print("No power benchmarks found in loaded results.") 
            return False


    @classmethod
    def compute_watt_seconds_per_query(cls, queries, attrs ):
        """
        Retreive the benchmark metric wspq.
        """
        return attrs["best_wspq"]

    @classmethod
    def run(cls, algo, X, distance, count, run_count, search_type, descriptor ):
        """The runner for power consumption is slightly different than the default runner."""

        capture_time = power_capture.min_capture_time
        best_search_time = descriptor["best_search_time"]

        inner_run_count = math.ceil(capture_time/best_search_time) if capture_time > best_search_time else 1

        print('Run for power capture with %d iterations (via %d/%f) for %d iterations'
            % (inner_run_count, capture_time, best_search_time, run_count ) )

        cap_ids = []
        power_run_counts = []
        power_run_times = []
        power_consumptions = []
        power_tot_queries = []

        best_power_cons = float('inf')
        for i in range(run_count):
            cap_id = cls.start()
            start = time.time()
            for i in range(inner_run_count):
                if search_type == "knn":
                    algo.query(X, count)
                else:
                    algo.range_query(X, count)
            total = (time.time() - start)
            power_stats = cls.stop(cap_id, all_stats=True)
            power_cons = power_stats['tot_power']
            tot_queries = inner_run_count * X.shape[0]

            # Track the best one thus far 
            best_power_cons = min(best_power_cons, power_cons)
            best_tot_queries = tot_queries # Although its always the same now, we may change that

            cap_ids.append(cap_id)
            power_run_counts.append( inner_run_count )
            power_run_times.append( total )
            power_consumptions.append( power_cons )
            power_tot_queries.append( tot_queries )

        power_cons_mean  = statistics.mean( power_consumptions )
        power_cons_stdev = statistics.stdev( power_consumptions )
        best_wspq = best_power_cons/best_tot_queries
        mean_wspq = power_cons_mean/best_tot_queries
        print("wspq: best=%f mean=%f best_tot_queries=%d" % (best_wspq, mean_wspq, best_tot_queries))
        power_stats = {"power_cap_id": cap_ids,
                 "power_run_count": power_run_counts,
                 "power_run_time":  power_run_times,
                 "power_consumption":power_consumptions,
                 "best_power_consumption": best_power_cons,
                 "inner_run_count": inner_run_count, 
                 "power_consumption_mean": power_cons_mean,
                 "power_consumption_stdev": power_cons_stdev,
                 "best_wspq": best_wspq,
                 "mean_wspq": mean_wspq }

        for k in power_stats.keys():
            descriptor[k] = power_stats[k]


#
# To run these unit tests for the power_capture class, type 'python power_capture.py'
#
if __name__ == "__main__":
    
    print("power capture unit tests")

    ipmicap_ip = "192.168.99.112" # Set to your ipmicap's server ip
    ipmicap_port = 3000 # Set to your ipmicap's server port
    min_capture_time = -1

    #power_capture( ipmicap_ip, ipmicap_port, min_capture_time )
    power_capture( "%s:%d:%f" % (ipmicap_ip, ipmicap_port, min_capture_time ))

    print("pinging ipmicap server at %s:%d" % (power_capture.ipmicap_ip, 
                                                power_capture.ipmicap_port))
    power_capture.ping()

    print("enabled=", power_capture.enabled())

    print("start")  
    cid=power_capture.start()
    print("cid=",cid)

    print("stop")   
    power_capture.stop()

    stats = power_capture.get_stats([cid])
    print("stats=",stats)

    print("all tests passed.")  

