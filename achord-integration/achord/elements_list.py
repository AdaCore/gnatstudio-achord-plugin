# This is a tree view that lists elements

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

# The columns in the model
COL_LABEL = 0
COL_FOREGROUND = 1
COL_ELEMENTTYPE = 2
COL_LOCATION = 3
COL_SOURCESTATUS = 4
COL_STATUS = 5
COL_URI = 6


class ElementList(object):

    def __init__(self, elements_list):
        """elements_list is a raw representation of elements, 
           as returned by Achord.
        """

        self.elements_list = elements_list

        # This is the tree model
        self.store = Gtk.TreeStore(
            str, # Label
            Gdk.RGBA, # Foregreound
            str, # ElementType
            str, # Location
            str, # SourceStatus
            str, # Status
            str, # URI
            )

        # The tree view
        self.view = Gtk.TreeView(self.store)
        self.view.set_name("elementlist_view")  # For debugging/testing

        # For now, render only the URI of the element
        self.uri_col = Gtk.TreeViewColumn("URI")
        cell = Gtk.CellRendererText()
        self.uri_col.pack_start(cell, True)
        self.uri_col.add_attribute(cell, "text", COL_URI)
        self.uri_col.add_attribute(cell, "foreground-rgba", COL_FOREGROUND)
        
        self.view.append_column(self.uri_col)

        self.default_fg = Gdk.RGBA(0, 0, 0)

        # Fill the model
        self.fill_model()

    def fill_model(self):
        """Fill the model from the elements dict"""
        for e in self.elements_list:
            it = self.store.append(None)
            self.store[it] = [
                "",  # Label is unused for now
                self.default_fg, # Foregreound
                e["location"], # Location
                e["elementType"], # ElementType
                e["sourceStatus"], # SourceStatus
                e["status"], # Status
                e["uri"], # URI
            ]