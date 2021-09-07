# Handles code elements

import os
import json

from connection import Payload

class CodeElement(object):
    
    def __init__(self, file, line, column, orig_text, sha1):
        self.file = file
        self.line = line
        self.column = column
        self.orig_text = orig_text
        self.sha1 = sha1

    def to_achord_save_payload(self):
        return {
            "uri": "achord://gnatstudio/ada/",
            "content": "1",
            "elementType": "code",
            "location: os.path.basename(self.file) + "#" + f"{self.line}",
            "status": "OK",
            "sourceStatus": "Single",
            "info": {
                "orig_text": self.orig_text,
            }
        }


def save_to_achord(connection, element_list):
    """Save a list of CodeElements to Achord"""
    payload = Payload("save",
        {
            "elements": [e.to_achord_save_payload() for e in element_list]
        }
    )

    result = connection.blocking_request(payload)

    # TODO: check the result