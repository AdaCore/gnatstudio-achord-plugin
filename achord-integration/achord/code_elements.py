# Handles code elements

import os
import re
import hashlib

from achord.raw_payload import Payload
from achord.project_support import make_path_project_relative


def parse_achord_location(location):
    """return (file, line) from an Achord location"""
    file, loc = location.split("#")
    return file, loc.split("-")[0]


class SubpDecl(object):
    def __init__(self, line, column, orig_text):
        """A subprogram decl. orig_text is the full text of the profile, encoded in utf-8"""
        self.line = line
        self.column = column
        self.orig_text = orig_text

        # Make an invariant hash of the profile spec

        # Replace any sequence of whitespaces/tabs/new lines with one space...
        self.condensed_text = re.sub("\s+", " ", orig_text)

        # ... and produce a hash of that.
        self.sha1 = hashlib.sha1(self.condensed_text.encode("utf-8")).hexdigest()

    def __repr__(self):
        return self.condensed_text


class AchordElement(object):
    """Straight mapping of Achord elements"""

    def __init__(self, elementType, location, uri, sourceStatus=None, status="OK"):
        """Parameters are Achord fields"""
        self.elementType = elementType
        self.location = location
        self.sourceStatus = sourceStatus
        self.status = status
        self.uri = uri
        self.file, self.line = parse_achord_location(location)

    def __repr__(self):
        return f"{self.uri}"


# Definitions of the status for elements
SYNC_UNKNOWN = "SYNC_UNKNOWN"  #   unknown (initial state)
SYNC_CONNECTED = "SYNC_CONNECTED"  # connected to source
SYNC_ORPHANED = (
    "SYNC_ORPHANED"
)  #  orphaned: we don't know which source object it belongs to


class CodeElement(AchordElement):
    def __init__(self, file, line, sha1):
        self.project_relative_filename = make_path_project_relative(file)
        super().__init__(
            "code",
            f"{self.project_relative_filename}#{line}",
            f"achord://gnatstudio/ada/{sha1}#1",
        )
        self.file = file
        self.sha1 = sha1
        self.sync_status = SYNC_UNKNOWN
        self.subp = None

    def to_achord_save_payload(self):
        return {
            "uri": self.uri,
            "content": "1",
            "elementType": self.elementType,
            "location": f"{os.path.basename(self.file)}#{self.line}",
            # TODO: add information?
            #            "info": {
            #                "orig_text": self.orig_text,
            #            }
        }

    def __repr__(self):
        return f"{self.elementType} {self.uri} {self.sync_status} {self.subp}"


def save_to_achord(connection, element_list):
    """Save a list of CodeElements to Achord"""
    payload = Payload(
        "save", {"elements": [e.to_achord_save_payload() for e in element_list]}
    )

    result = connection.blocking_request(payload)

    # TODO: check the result
