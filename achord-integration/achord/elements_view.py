"""The GNAT Studio Achord Elements View"""

import GPS
from achord.elements_list import ElementList
from modules import Module


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
            default = GPS.Preference("Src-Editor-Reference-Style").get()
            highlight = GPS.Preference("Src-Editor-Keywords-Variant").get()
            self.element_list.preferences_changed(
                default.split("@")[1], highlight.split("@")[1]
            )

    def on_view_destroy(self):
        self.element_list = None

    def create_view(self):
        self.element_list = LAL_View_Widget()
        return self.element_list.box
