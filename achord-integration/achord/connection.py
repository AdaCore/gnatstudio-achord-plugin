"""Handles the connection to the Achord server"""

import zmq
import json

from achord.raw_payload import Payload
from achord.code_elements import AchordElement, CodeElement, parse_achord_location
from achord.achord_connection import log


class ConnectionMonitor(object):
    """Establishes, then monitors, the connection to Achord.
    """

    def __init__(self, requests_url, element_hook=None):
        """requests_url is a string of the form "<protocol>://<host>:port" """
        self.url = requests_url
        self.socket = None
        self.elements = []  # The downloaded elements
        self.element_hook = element_hook

    def connect(self):
        """Attempt a connection. Return a string containing the error if
           there was one, None otherwise"""
        try:
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.REQ)
            self.connection = self.socket.connect(self.url)
            self.poller = zmq.Poller()
            self.poller.register(self.socket)
        except Exception as inst:
            self.context = None
            self.socket = None
            self.connection = None
            self.poller = None
            return f"Exception occurred: {type(inst)} {inst}"

    def error(self):
        """Return the error stored in self, None if there isn't one"""
        pass

    def is_alive(self):
        """Return True if the connection is alive"""
        # Right now, there isn't a request made for hearbeat monitoring:
        # we use a "delete" request for a non-existent id instead.
        # TODO: replace this with a hearbeat monitoring request when it
        # is implemented.

        if self.socket is None:
            return False

        dummy = Payload("delete", {"_id": "__gnatstudio_non_existent_id"})
        try:
            result = self.blocking_request(dummy)
        except zmq.error.ZMQError:
            # This indicates that the connection is down
            return False

        return result and result["errorCode"] == "NoError"

    def close(self):
        """Close the connection"""
        self.poller.unregister(self.socket)  # ??? needed?
        self.socket.close()

    def download_all_elements(self):
        # Cleanup the previously stored elements
        log("Downloading elements... ", add_lf=False)
        self.elements = []

        # Request all elements from Achord
        get_elements = Payload(
            "getElements",
            {
                "elementSelection": [
                    {
                        "pathAttr": "elementType",
                        "pathMatcher": "glob",
                        "elements": ["**"],
                    }
                ]
            },
        )
        result = self.blocking_request(get_elements)
        num_code_elements = 0
        if not "elements" in result:
            # TODO: log a message
            return
        for el in result["elements"]:
            if (
                el["uri"].startswith("achord://gnatstudio")
                and el["elementType"] == "code"
            ):
                file, line = parse_achord_location(el["location"])
                sha1 = el["uri"].split("/")[-1][:-2]
                self.elements.append(CodeElement(file, line, sha1))
                num_code_elements += 1
            else:
                self.elements.append(
                    AchordElement(
                        el["elementType"],
                        el["location"],
                        el["uri"],
                        el["sourceStatus"],
                        el["status"],
                    )
                )
        num = len(el)
        log(f"[{num}] Elements received, including {num_code_elements} code element(s)")
        if self.element_hook is not None:
            self.element_hook()

    def blocking_request(self, payload, timeout=1000):
        """Send a request to the socket and block while waiting for the
           response.
           
           payload is a Payload object.

           returns a json dict of the corresponding response - and False if
           the response is invalid.
        """
        raw_bytes = bytes(json.dumps(payload.to_dict()), "utf-8")
        socks = dict(self.poller.poll(timeout))
        if socks:
            if socks.get(self.socket) == zmq.POLLOUT:
                self.socket.send(raw_bytes)
        socks = dict(self.poller.poll(timeout))
        response = {}
        if socks:
            if socks.get(self.socket) == zmq.POLLIN:
                raw_response = self.socket.recv()
                response = json.loads(raw_response)

        if "result" in response:
            return response["result"]
        else:
            return False
