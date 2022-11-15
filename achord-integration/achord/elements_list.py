# This is a tree view that lists elements

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

# The columns in the model
COL_LABEL = 0
COL_FOREGROUND = 1
COL_ELEMENTTYPE = 2
COL_LOCATION = 3
COL_URI = 4
COL_SOURCESTATUS = 5
COL_STATUS = 6


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
            str,  # Source Status
            str,  # Status
        )

        # The tree view
        self.view = Gtk.TreeView(self.store)
        self.view.set_name("elementlist_view")  # For debugging/testing

        def add_col(title, id):
            """Add a Gtk.TreeViewColumn for the given title and column id.
            return the col and the cell renderer."""
            col = Gtk.TreeViewColumn(title)
            cell = Gtk.CellRendererText()
            col.pack_start(cell, True)
            col.add_attribute(cell, "text", id)
            col.add_attribute(cell, "foreground-rgba", COL_FOREGROUND)
            col.set_sort_column_id(id)
            self.view.append_column(col)
            return col, cell

        # The URI
        col, cell = add_col("URI", COL_URI)
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        col.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col.set_expand(True)
        col.set_resizable(True)

        # The type
        add_col("Type", COL_ELEMENTTYPE)

        # The location
        add_col("Location", COL_LOCATION)

        # The source status
        add_col("Source Status", COL_SOURCESTATUS)

        # The status
        add_col("Status", COL_STATUS)

        self.default_fg = Gdk.RGBA(0, 0, 0)
        self.highlight_fg = Gdk.RGBA(255, 0, 0)

        # Pack widgets in a box
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.view)

        self.box = Gtk.VBox()

        # The filter box
        hbox = Gtk.HBox()
        label = Gtk.Label("Filter: ")
        hbox.pack_start(label, False, False, 3)
        self.entry = Gtk.Entry()
        hbox.pack_start(self.entry, True, True, 3)
        button = Gtk.Button("Filter")
        button.connect("clicked", lambda _: self.refresh(self.elements_list))
        hbox.pack_start(button, False, False, 3)
        button = Gtk.Button("Clear")
        button.connect("clicked", lambda _: self.clear_filter_and_refresh())
        hbox.pack_start(button, False, False, 3)
        self.filter_label = Gtk.Label("")
        self.filter_label.set_justify(Gtk.Justification.RIGHT)
        self.filter_label.set_alignment(1.0, 0.5)
        hbox.pack_start(self.filter_label, False, False, 3)
        self.box.pack_start(hbox, False, False, 3)
        self.box.pack_start(scroll, True, True, 0)

        # Fill the model
        self.fill_model()

    def clear_filter_and_refresh(self):
        """Clear the filter and refresh the list"""
        self.entry.set_text("")
        self.refresh(self.elements_list)

    def refresh(self, elements_list):
        self.elements_list = elements_list
        self.store.clear()
        self.fill_model()

    def fill_model(self):
        """Fill the model from the elements dict"""
        filter = self.entry.get_text()
        elements_filtered_out = 0
        for e in self.elements_list:
            # Apply the filter, if any
            if filter.strip() != "":
                if not (filter in e.uri + e.elementType + e.location):
                    elements_filtered_out += 1
                    continue
            it = self.store.append(None)
            self.store[it] = [
                "",  # Label is unused for now
                self.default_fg,  # Foregreound
                e.elementType,
                e.location,
                e.uri,  # URI
                e.sourceStatus,
                e.status,
            ]
        total = len(self.elements_list)
        self.filter_label.set_text(
            f"({total} elements, {elements_filtered_out} filtered out)"
        )

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
