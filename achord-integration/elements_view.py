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
        GPS.Hook("achord_elements_received").add(self.refresh_view)

    def setup(self):
        # Create an "open Libadalang" action
        make_interactive(self.get_view, category="Views", name="open Achord Elements")

    def preferences_changed(self, name="", pref=None):
        if self.element_list:
            self.element_list.preferences_changed()

    def on_view_destroy(self):
        self.element_list = None

    def refresh_view(self, hook_name=""):
        if self.element_list:
            self.element_list.refresh(get_achord_elements())

    def create_view(self):
        self.element_list = ElementListWidget()
        self.refresh_view()
        return self.element_list.box

    def save_desktop(self, child):
        """Save the contents of the view in the desktop"""
        return self.name()

    def load_desktop(self, data):
        """Restore the contents from the desktop"""
        return self.get_child()
