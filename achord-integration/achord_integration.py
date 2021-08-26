"""Achord / GNAT Studio integration plugin """

import GPS
from extensions.private.xml import X
from modules import Module

from achord.connection import ConnectionMonitor, Payload

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

    def __init__(self):
        self.connection = None
        self.log = []
        # The text log, one entry par call to log()

        super(Module, self).__init__()

    def open_console(self):
        """Open the Achord integration console"""
        self.console = GPS.Console("Achord")

    def log(self, message, add_lf=True):
        self.open_console()
        m = message + ("\n" if add_lf else "")
        self.log.append(m)
        self.console.write(m)

    def connect_to_achord(self, url):
        """Attempt to connect to the Achord server"""
        self.connection = ConnectionMonitor(url)
        error = self.connection.connect()
        if error:
            self.log(f"Error when connecting: {error}")
        if self.connection.is_alive():
            self.log(f"Connection established on {url}.")
        else:
            self.log(f"Could not establish connection on {url}.")

    def setup(self):
        self.load_project()

    def project_view_changed(self):
        self.load_project()

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


# Log the fact that the plugin was loaded
msg("Achord integration plugin loaded successfully.")
