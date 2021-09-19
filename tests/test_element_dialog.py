import gi
from achord.connection import ConnectionMonitor
from achord.element_info_dialog import ElementInfoDialog
from achord.code_elements import SubpDecl, AchordElement

# Establish a connection
m = ConnectionMonitor("tcp://localhost:5555")
m.connect()
assert m.is_alive()
m.download_achord_db()

subp = SubpDecl(12, 11, "hello")

d = ElementInfoDialog(subp, m.elements)

print(d.run())
