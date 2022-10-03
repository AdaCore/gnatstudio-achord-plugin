"""Achord / GNAT Studio integration plugin """

import GPS

from gs_utils import make_interactive
from extensions.private.xml import X
from modules import Module

from achord.connection import ConnectionMonitor
from achord.editor_actions import decorate_editor

# This encodes the XML description of the Achord project attributes
PROJECT_ATTRIBUTES = [
    X(
        "project_attribute",
        package="IDE",
        name="Achord_Server_Address",
        label="Achord Server Address",
        description=(
            "The URL for the Achord Response Socket,\n"
            "for instance tcp://localhost:5555"
        ),
        editor_page="Achord",
        editor_section="Connection",
        hide_in="wizard library_wizard",
    ).children(X("string")),
    X(
        "project_attribute",
        package="IDE",
        name="Achord_Publish_Address",
        label="Achord Publish Address",
        description=(
            "The URL for the Achord Publish Socket,\n"
            " for instance tcp://localhost:7777"
        ),
        editor_page="Achord",
        editor_section="Connection",
        hide_in="wizard library_wizard",
    ).children(X("string")),
]

PROJECT_HELP = """
To add support for connecting to Achord, modify your project
file to contain an attribute "Achord_Server_Address" in the "IDE"
package. For instance:

   package IDE is
      for Achord_Server_Address use "tcp://localhost:5555";
   end IDE;

"""

# Load the project attributes
def list_to_xml(items):
    return "\n".join(str(i) for i in items)


def msg(message, add_lf=True):
    """Print a message on the GNAT Studio Messages view"""
    GPS.Console().write(message + ("\n" if add_lf else ""))


GPS.parse_xml(list_to_xml(PROJECT_ATTRIBUTES))


class Achord_Integration(Module):
    """The main module for this plugin"""

    def __init__(self):
        self.connection = None
        self.accumulated_log = []
        # The text log, one entry par call to log()

        super(Module, self).__init__()

    def setup(self):
        # Create menus when this module is setup.
        # It is better to call make_interactive here than use the @interactive
        # decorator on the method. The latter would take effect even if the
        # module is never initialized.

        make_interactive(self.open_console, menu="/Achord/Open Achord Log")

        make_interactive(self.open_elements, menu="/Achord/Open Achord Elements")

        make_interactive(self.synchronise, menu="/Achord/Synchronise")

        make_interactive(self.disconnect, menu="/Achord/Disconnect From Server")

        make_interactive(self.load_project, menu="/Achord/Connect to Server")

        make_interactive(self.create_code_element, menu="/Achord/Create Code Element")

        make_interactive(self.annotate_editor, menu="/Achord/Annotate Editor")

        make_interactive(
            self.remove_editor_annotations, menu="/Achord/Remove Editor Annotations"
        )

        make_interactive(self.create_link, menu="/Achord/Create Link")

        self.load_project()

    def disconnect(self):
        """Close the connection to Achord"""
        if self.connection is not None:
            self.connection.close()

    def annotate_editor(self):
        """Open the elements view"""
        GPS.Console().write("NOT IMPLEMENTED\n")

    def remove_editor_annotations(self):
        """Open the elements view"""
        GPS.Console().write("NOT IMPLEMENTED\n")

    def create_link(self):
        """Create a link from an Achord Element to a Code Element"""
        GPS.Console().write("NOT IMPLEMENTED\n")

    def create_code_element(self):
        """Open the elements view"""
        GPS.Console().write("NOT IMPLEMENTED\n")

    def open_elements(self):
        """Open the elements view"""
        GPS.execute_action("open Achord Elements")

    def synchronise(self):
        """Open the elements view"""
        GPS.Console().write("NOT IMPLEMENTED\n")

    def open_console(self):
        """Open the Achord integration console"""
        self.console = GPS.Console("Achord Log")

    def log(self, message, add_lf=True):
        self.open_console()
        m = message + ("\n" if add_lf else "")
        self.accumulated_log.append(m)
        self.console.write(m)

    def on_elements_received(self):
        """Called when elements are received. This runs the corresponding hook."""
        GPS.Hook("achord_elements_received").run()

    def connect_to_achord(self, url):
        """Attempt to connect to the Achord server"""
        if self.connection is not None:
            self.connection.close()

        self.connection = ConnectionMonitor(url, self.on_elements_received)
        error = self.connection.connect()
        if error:
            self.log(f"Error when connecting: {error}")
        if self.connection.is_alive():
            self.log(f"Connection established on {url}.")
            self.connection.download_achord_db()
        else:
            self.log(f"Could not establish connection on {url}.")

    def project_view_changed(self):
        """Called automatically when the project has changed"""
        self.load_project()

    def file_edited(self, file):
        buf = GPS.EditorBuffer.get(file)
        decorate_editor(buf)

    def buffer_edited(self, file):
        buf = GPS.EditorBuffer.get(file)
        decorate_editor(buf)

    def load_project(self):
        """Called when the project view has changed"""
        p = GPS.Project.root()

        self.log(f"Loaded '{p.file().name()}'")

        # Retrieve the server address specified in the project
        url = p.get_attribute_as_string("Achord_Server_Address", package="IDE")

        if url:
            self.connect_to_achord(url)
        else:
            self.log("Achord not set up for this project.")
            self.log(PROJECT_HELP)


# Register the hooks
# "on_elements_received": called when elements are received.
GPS.Hook.register("achord_elements_received", "simple_hooks")

# Log the fact that the plugin was loaded
msg("Achord integration plugin loaded successfully.")
