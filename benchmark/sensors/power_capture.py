import requests
import uuid
import json

class power_capture:

    """
    This class provides various capabilites related to the T3 track
    of the Big ANN Competition for NeurIPS 2021:
        * communicates with an ipmicap server ( see http://github.com/fractalsproject/ipmicap )
        * leverage's servers power sensor capture abilities
        * retrieves power statistics computed by the serer
    """
    
    ipmicap_ip          = None
    ipmicap_port        = None
    min_capture_time    = None
    raise_exc_on_fail   = None
    started             = False
    algo                = None
    dataset             = None
    arguments           = None
    query_arguments     = None
    current_id          = None

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
        ret = requests.get(url,parms)
        if ret.status_code!=200:
            msg = "T3: Failed to ping ipmicapserver."
            if cls.raise_exc_on_fail: 
                raise Exception(msg)
            else: 
                print("Power: Failed to ping ipmicap server.")
                return False
        else: 
            return True
    
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
    def start(cls): #, algo, dataset, arguments, query_arguments):
        """
        Start power capture at the IPMI server.
        """
        #cls.algo = algo
        #cls.dataset = dataset
        #cls.arguments = arguments
        #cls.query_arguments = query_arguments
        cls.current_id = str(uuid.uuid4())
        status = cls._send_msg_to_ipmicap_server("log",
            {"start":1,"id":cls.current_id})
        if status:
            cls.started = True
            return cls.current_id
        else:
            return False

    @classmethod
    def stop(cls):
        """
        End power capture at the IPMI server.
        """
        if not cls.started:
            print("Power: Capture recording not started.")  
            return False
        
        status =  cls._send_msg_to_ipmicap_server("log",
            {"stop":0, "id":cls.current_id})
        if status:
            cls.started = False 
            return True
        else:
            return False

    @classmethod
    def get_stats(cls, capture_ids):
        """
        Retrieve power capture statistics for capture ids supplied.
        """
        stats = {}
        for cid in capture_ids:
            stats[cid]=0
        return stats
        #status =  cls._send_msg_to_ipmicap_server("stats",
        #    {"stop":0, "id":cls.current_id})
        

#
# To run these unit tests for the T3 class, type 'python t3.py'
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
    cid=power_capture.start() #"algo","dataset",['euclidean',8192],50 )
    print("cid=",cid)

    print("stop")   
    power_capture.stop()

    stats = power_capture.get_stats([cid])
    print("stats=",stats)

    print("all tests passed.")  

