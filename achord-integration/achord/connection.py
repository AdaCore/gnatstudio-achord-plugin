"""Handles the connection to the Achord server"""

import zmq
import json

PLUGIN_IDENTIFIER = "gnatstudio"

global_id = 1
# Global counter for request IDs


class Payload(object):
    """A high-level raw representation of a jsonrpc payload.
       Auto fills the "jsonrpc" field and the "id" field via  """

    def __init__(self, method, params):
        self.method = method
        self.params = params

        self.params["pluginIdentifier"] = PLUGIN_IDENTIFIER
        global global_id
        self.id = global_id
        global_id += 1

    def to_dict(self):
        """Return a raw dict version of self"""
        return {
            "method": self.method,
            "params": self.params,
            "jsonrpc": "2.0",
            "id": self.id,
        }


class ConnectionMonitor(object):
    """Establishes, then monitors, the connection to Achord.
    """

    def __init__(self, requests_url):
        """requests_url is a string of the form "<protocol>://<host>:port" """
        self.url = requests_url

    def connect(self):
        """Attempt a connection. Return a string containing the error if
           there was one, None otherwise"""
        try:
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.REQ)
            self.connection = self.socket.connect(self.url)
        except Exception as inst:
            self.context = None
            self.socket = None
            self.connection = None
            return(f"Exception occurred: {type(inst)} {inst}")

    def error(self):
        """Return the error stored in self, None if there isn't one"""

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

        return result and result["errorCode"] == "NoError"

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
        raw_bytes = bytes(json.dumps(payload.to_dict()), "utf-8")
        self.socket.send(raw_bytes)
        raw_response = self.socket.recv()
        response = json.loads(raw_response)
        if "result" in response:
            return response["result"]
        else:
            return False
