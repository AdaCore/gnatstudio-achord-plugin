# This is a tree view that lists elements

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

# The columns in the model
COL_LABEL = 0
COL_FOREGROUND = 1
COL_ELEMENTTYPE = 2
COL_LOCATION = 3
COL_URI = 4


class ElementListWidget(object):
    def __init__(self):
        """A widget for listing elments.

           elements_list is a list of AchordElements.
        """

        self.elements_list = []

        # This is the tree model
        self.store = Gtk.TreeStore(
            str,  # Label
            Gdk.RGBA,  # Foregreound
            str,  # ElementType
            str,  # Location
            str,  # URI
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
        self.highlight_fg = Gdk.RGBA(255, 0, 0)

        # Fill the model
        self.fill_model()

        # Pack widgets in a box
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.view)

        self.box = Gtk.VBox()
        self.box.pack_start(scroll, True, True, 0)

    def refresh(self, elements_list):
        self.elements_list = elements_list
        self.store.clear()
        self.fill_model()

    def fill_model(self):
        """Fill the model from the elements dict"""
        for e in self.elements_list:
            it = self.store.append(None)
            self.store[it] = [
                "",  # Label is unused for now
                self.default_fg,  # Foregreound
                e.location,
                e.elementType,
                e.uri,  # URI
            ]

    def get_selected_uri(self):
        """Return the URI of the selected element, None if there isn't one"""
        sel = self.view.get_selection()
        rows = sel.get_selected_rows()
        (model, pathlist) = sel.get_selected_rows()
        if pathlist:
            tree_iter = model.get_iter(pathlist[0])
            return model.get_value(tree_iter, COL_URI)

        return None

    def preferences_changed(self, default_fg, highlight_fg):
        """Apply the contents of the preferences"""
        prev = (self.default_fg, self.highlight_fg)
        self.default_fg.parse(default_fg)
        self.highlight_fg.parse(highlight_fg)
        if prev != (self.default_fg, self.highlight_fg):
            # The colours have changed, re-fill the model
            self.store.clear()
            self.fill_model()


class ElementSelectionDialog(object):
    """A dialog showing a list of elements, allowing the user to choose one."""

    def __init__(self, elements):
        self.elements = elements
        self.dialog = Gtk.Dialog()
        self.dialog.set_title("Choose an Element")
        self.elementlist = ElementListWidget()
        self.elementlist.refresh(self.elements)

        self.dialog.get_content_area().pack_start(self.elementlist.box, True, True, 3)
        self.dialog.set_default_size(400, 200)

        self.dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

    def run(self):
        """Launch the dialog and return the selected element if any, None otherwise."""
        self.dialog.show_all()
        response = self.dialog.run()
        if response == Gtk.ResponseType.CANCEL:
            self.dialog.destroy()
            return None

        uri = self.elementlist.get_selected_uri()
        self.dialog.destroy()
        if uri is None:
            return None

        for x in self.elements:
            if x.uri == uri:
                return x

        return None
