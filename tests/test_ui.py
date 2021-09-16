from achord.connection import ConnectionMonitor, Payload
from achord.elements_list import ElementList

from gi.repository import Gtk

# Establish a connection
m = ConnectionMonitor("tcp://localhost:5555")
m.connect()
assert m.is_alive()

# Check retrieving the list of elements

get_elements = Payload(
    "getElements",
    {
        "elementSelection": [
            {"pathAttr": "elementType", "pathMatcher": "glob", "elements": ["**"]}
        ]
    },
)
result = m.blocking_request(get_elements)

el = ElementList(result["elements"])

m.close()
assert not m.is_alive()

w = Gtk.Window()
w.add(el.view)
w.show_all()

Gtk.main()
