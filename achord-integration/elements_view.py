"""The GNAT Studio Achord Elements View"""

import GPS
from achord.elements_list import ElementListWidget
from achord.achord_connection import get_achord_connection
from achord.connection import Payload

from modules import Module
from gs_utils import make_interactive


class Elements_View(Module):
    """ A GS module, providing the Achord Elements View"""

    view_title = "Achord Elements"
    mdi_position = GPS.MDI.POSITION_RIGHT

    def __init__(self):
        self.element_list = None

    def setup(self):
        # Create an "open Libadalang" action
        make_interactive(self.get_view, category="Views", name="open Achord Elements")

    def preferences_changed(self, name="", pref=None):
        if self.element_list:
            self.element_list.preferences_changed()

    def on_view_destroy(self):
        self.element_list = None

    def create_view(self):
        connection = get_achord_connection()
        msg = None
        if connection is None:
            msg = "No Achord connection available - connect to Achord first."
        else:
            if not connection.is_alive():
                msg = "The connection to Achord is not alive."

        if msg is not None:
            GPS.Console().write(f"{msg}\n", mode="error")
            return None

        # TODO: move this to a centralised place
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
        result = connection.blocking_request(get_elements)

        # TODO: add error handling for the contents of result
        self.element_list = ElementListWidget(result["elements"])
        return self.element_list.box
