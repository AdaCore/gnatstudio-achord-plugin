"""Defines a dialog saying what to do with a given element"""

from os import link
from gi.repository import Gtk
from achord.achord_connection import get_achord_connection, log
from achord.code_elements import (
    CodeElement,
    create_link,
    delete_link,
    delete_element,
    save_to_achord,
)
from achord.elements_list import ElementSelectionDialog
from gi.repository.GLib import markup_escape_text


class ElementInfoDialog(object):
    def __init__(self):
        """subp is a SubpDecl, elements a list of AchordElement"""
        self.subp = None
        self.elements = None
        self.link_types = None
        self.dialog = Gtk.Dialog()

        self.dialog.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

        vbox = Gtk.VBox()
        hbox = Gtk.HBox()
        hbox.pack_start(vbox, True, True, 10)
        self.dialog.get_content_area().add(hbox)
        self.subp_label = Gtk.Label()
        self.subp_label.set_alignment(0.0, 0.0)
        vbox.pack_start(self.subp_label, False, False, 3)

        self.status_label = Gtk.Label()
        self.status_label.set_alignment(0.0, 0.0)
        vbox.pack_start(self.status_label, False, False, 3)

        action_buttons = Gtk.VButtonBox(True)
        vbox.pack_start(action_buttons, True, True, 3)

        self.connect_button = Gtk.Button("Add a trace...")
        self.connect_button.connect(
            "clicked", lambda x, y: self.on_connect_clicked(x, y), True
        )
        action_buttons.add(self.connect_button)

        self.disconnect_button = Gtk.Button("Disconnect")
        self.disconnect_button.connect(
            "clicked", lambda x, y: self.on_disconnect_clicked(x, y), True
        )

        action_buttons.add(self.disconnect_button)

    def on_connect_clicked(self, button, flag):
        """Called when the "Add a trace..." button is clicked"""
        # Present a selection dialog
        selected_element = ElementSelectionDialog(self.elements).run()
        if selected_element is None:
            return

        # An element was selected - we need to do two things:
        # create the Code Element for this subprogram, then link it to the
        # selected element.
        code_element = CodeElement(self.subp.file, self.subp.line, self.subp.sha1)
        connection = get_achord_connection()
        if connection is None:
            log("Achord connection not available")
            return
        save_to_achord(connection, [code_element])

        # Find out which link types match
        matching_link_type = None
        for l in self.link_types:
            if selected_element in l.possible_sources_for_element(
                self.elements, code_element
            ):
                matching_link_type = l.typeName
                break
            # TODO: handle the case where multiple link types match

        if matching_link_type is None:
            log(
                f"Couldn't find a link type from {selected_element.elementType} to {code_element.elementType}"
            )
        else:
            create_link(connection, selected_element, code_element, matching_link_type)
        self.subp.connected_element = code_element
        connection.download_achord_db()
        self.refresh(self.subp, connection.elements, connection.link_types)

    def on_disconnect_clicked(self, button, flag):
        """Called when the "Disconnect" button is clicked"""
        connection = get_achord_connection()
        if connection is None:
            log("Achord connection not available")
            return

        if self.subp.connected_element is None:
            return

        # First delete the links
        for link_type, source_element in list(self.subp.connected_element.links_from):
            delete_link(
                connection, source_element, self.subp.connected_element, link_type
            )

        # And delete the element
        delete_element(connection, self.subp.connected_element)
        self.subp.connected_element = None
        connection.download_achord_db()
        self.refresh(self.subp, connection.elements, connection.link_types)

    def refresh(self, subp, elements, link_types):
        self.subp = subp
        self.elements = elements
        self.link_types = link_types
        self.subp_label.set_markup(
            '<b>Entity:</b> <span face="monospace">'
            + markup_escape_text(self.subp.orig_text)
            + "</span>"
        )
        status = ""
        if self.subp.connected_element is None:
            status = "not traced to Achord"
            self.connect_button.set_sensitive(True)
            self.disconnect_button.set_sensitive(False)
        else:
            if len(self.subp.connected_element.links_from) == 0:
                status = (
                    "<b>possible issue:</b> element present but no trace established."
                )
                self.connect_button.set_sensitive(False)
                self.disconnect_button.set_sensitive(True)
            else:
                for linkType, element in self.subp.connected_element.links_from:
                    status += (
                        "<u>"
                        + markup_escape_text(linkType)
                        + "</u> "
                        + markup_escape_text(element.uri)
                        + "\n"
                    )
                self.connect_button.set_sensitive(False)
                self.disconnect_button.set_sensitive(True)

        self.status_label.set_markup("<b>Status:</b> " + status)

    def run(self):
        """Run the dialog, and return a tuple (operation_to_do, target_element)"""
        self.dialog.show_all()
        response = self.dialog.run()
        self.dialog.destroy()
        return response  # TODO return the right info
