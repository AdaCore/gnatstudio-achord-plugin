"""Achord / GNAT Studio integration plugin """

import GPS
from extensions.private.xml import X
from modules import Module

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

# Load the project attributes
def list_to_xml(items):
    return "\n".join(str(i) for i in items)


def msg(message, add_lf=True):
    """Print a message on the GNAT Studio Messages view"""
    GPS.Console().write(message + ("\n" if add_lf else ""))


GPS.parse_xml(list_to_xml(PROJECT_ATTRIBUTES))


class Achord_Integration(Module):
    def open_console(self):
        """Open the Achord integration console"""
        self.console = GPS.Console("Achord")

    def log(self, message, add_lf=True):
        self.open_console()
        self.console.write(message + ("\n" if add_lf else ""))

    def connect_to_achord(self, url):
        """Attempt to connect to the Achord server"""

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
            self.log("Achord not set up")
            # TODO: add a more informative message


# Log the fact that the plugin was loaded
msg("Achord integration plugin loaded successfully.")
