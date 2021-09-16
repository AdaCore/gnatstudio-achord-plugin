from achord.connection import ConnectionMonitor, Payload
from achord.code_elements import CodeElement, save_to_achord

# Establish a connection
m = ConnectionMonitor("tcp://localhost:5555")
m.connect()
assert m.is_alive()


# Check retrieving the list of elements
m.download_all_elements()

original_element_count = len(m.elements)

# Add an element
e = CodeElement("hello.adb", 1, "a0a0a0")

save_to_achord(m, [e])

m.download_all_elements()

# Check that the element is now in the database
assert len(m.elements) == original_element_count + 1

# Download all the link types
m.download_all_link_types()
assert len(m.link_types) == 2

# check the link types mapping
matches = []
for link_type in m.link_types:
    matches.append(
        (link_type.coTypeName, link_type.possible_sources_for_element(m.elements, e))
    )

assert matches == [("SatisfiedBy", []), ("ImplementedBy", [m.elements[2]])]
m.close()
assert not m.is_alive()
print("SUCCESS")
