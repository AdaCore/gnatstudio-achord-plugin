import gi
from achord.achord_connection import testsuite_set_achord_connection
from achord.connection import ConnectionMonitor
from achord.element_info_dialog import ElementInfoDialog
from achord.code_elements import SubpDecl, AchordElement, save_to_achord

# Establish a connection
m = ConnectionMonitor("tcp://localhost:5555")
m.connect()
testsuite_set_achord_connection(m)
assert m.is_alive()

# req = AchordElement(
#    "reqif/Requirement", "req_location#123", "achord://gnatstudio/requirement#1"
# )
# save_to_achord(m, [req])

m.download_achord_db()

subp = SubpDecl("hello.adb", 12, 11, "hello")
for x in m.elements:
    print(x)
d = ElementInfoDialog()
d.refresh(subp, m.elements, m.link_types)

print(d.run())
