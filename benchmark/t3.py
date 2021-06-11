import requests

class T3:

	"""
	This class provides various capabilites related to the T3 track
	of the Big ANN Competition for NeurIPS 2021.
	"""

	def __init__(self, ipmicap_ip, ipmicap_port, raise_exc_on_fail=True):

		self.ipmicap_ip = ipmicap_ip
		self.ipmicap_port = ipmicap_port
		self.raise_exc_on_fail = raise_exc_on_fail


	def _send_msg_to_ipmicap_server(self, uri, parms):

		url = "http://%s:%d/%s" % (self.ipmicap_ip,self.ipmicap_port,uri)
		ret = requests.get(url,parms)
		if ret.status_code!=200:
			msg = "T3: Failed to ping ipmicapserver."
			if self.raise_exc_on_fail: 
				raise Exception(msg)
			else: 
				print("T3: Failed to ping ipmicap server.")
				return False
		else: 
			return True


	def ping_ipmicap_server(self):
		"""
		Ping the IPMICAP server and make sure it's running.
		"""

		return self._send_msg_to_ipmicap_server("log",{"ping":1})


	def start_query_set(self):
		"""
		Log the start of a query set at the IPMICAP server.
		"""

		return self._send_msg_to_ipmicap_server("log",{"query_set":1})


	def end_query_set(self):
		"""
		Log the end of a query set at the IPMICAP server.
		"""

		return self._send_msg_to_ipmicap_server("log",{"query_set":0})

	
#
# To run these unit tests for the T3 class, type 'python t3.py'
#
if __name__ == "__main__":
	
	print("t3 lib unit tests")

	ipmicap_ip = "192.168.99.112" # Set to your ipmicap's server ip
	ipmicap_port = 3000 # Set to your ipmicap's server port

	t3 = T3(ipmicap_ip, ipmicap_port)

	print("pinging ipmicap server at %s:%d" % (ipmicap_ip, ipmicap_port))
	t3.ping_ipmicap_server()

	print("start query set")	
	t3.start_query_set()

	print("end query set")	
	t3.end_query_set() 

	print("all tests passed.")	

