# Defines a high-level abstraction for a zmq request payload

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