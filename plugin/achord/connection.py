"""Handles the connection to the Achord server"""

import zmq
import json


global_id = 1
# Global counter for request IDs

class Payload(object):
    """A high-level raw representation of a jsonrpc payload.
       Auto fills the "jsonrpc" field and the "id" field via  """

    def __init__(self, method, params):
        self.method = method
        self.params = params
        global global_id
        self.id = global_id
        global_id += 1

    def to_dict(self):
        """Return a raw dict version of self"""
        return {"method": self.method, 
                "params": self.params, 
                "jsonrpc": "2.0",
                "id": self.id}



class ConnectionMonitor(object):
    """Establishes, then monitors, the connection to Achord.
    """

    def __init__(self, requests_url):
        """Establishes a connection.
           requests_url is a string of the form "<protocol>://<host>:port"
        """
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.connection = self.socket.connect(requests_url)

    def is_alive(self):
        """Return True if the connection is alive"""
        # Right now, there isn't a request made for hearbeat monitoring:
        # we use a "delete" request for a non-existent id instead.
        # TODO: replace this with a hearbeat monitoring request when it
        # is implemented.
        dummy = Payload("delete", {"_id": "__gnatstudio_non_existent_id"})
        try:
            result = self.blocking_request(dummy)
        except zmq.error.ZMQError:
            # This indicates that the connection is down
            return False
        
        return result and 'result' in result

    def close(self):
        """Close the connection"""
        self.socket.close()

    def blocking_request(self, payload):
        """Send a request to the socket and block while waiting for the
           response.
           
           payload is a Payload object.

           returns a json dict of the corresponding response - and False if
           the response is invalid.
        """
        raw_bytes = bytes(json.dumps(payload.to_dict()), 'utf-8')
        self.socket.send(raw_bytes)
        raw_response = self.socket.recv()
        return json.loads(raw_response)
