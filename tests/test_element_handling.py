from achord.connection import ConnectionMonitor, Payload
from achord.code_elements import CodeElement, save_to_achord

# Establish a connection
m = ConnectionMonitor("tcp://localhost:5555")
m.connect()
assert(m.is_alive())


# Check retrieving the list of elements
get_elements = Payload(
    "getElements",
    {"elementSelection": [
                        {
                          "pathAttr": "elementType",
                          "pathMatcher": "glob",
                          "elements": [
                            "**"
                          ]
                        }]
    }
)
result = m.blocking_request(get_elements)

original_element_count = len(result["elements"])


# Add an element
e = CodeElement("hello.adb", 1, 1, "procedure foo;", "a0a0a0")

save_to_achord(m, [e])

# Check that the element is now in the database
result = m.blocking_request(get_elements)
assert(len(result["elements"]) == original_element_count + 1)

m.close()
assert(not m.is_alive())
print("SUCCESS")