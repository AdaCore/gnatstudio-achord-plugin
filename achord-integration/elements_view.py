"""The GNAT Studio Achord Elements View"""

import GPS
from achord.elements_list import ElementListWidget
from achord.achord_connection import get_achord_elements
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
        self.element_list = ElementListWidget(get_achord_elements())
        return self.element_list.box
