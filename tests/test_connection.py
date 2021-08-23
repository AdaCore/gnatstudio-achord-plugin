from achord.connection import ConnectionMonitor, Payload

# Establish a connection
m = ConnectionMonitor("tcp://localhost:5555")
assert(m.is_alive())

# Create two dummy payloads
p1 = Payload("delete", {
    "uri": "achord://gnatstudio/subprogram/doesnotexist",
    "pluginIdentifier": "GNATStudio"})
p2 = Payload("delete", {
    "uri": "achord://gnatstudio/subprogram/doesnotexist",
    "pluginIdentifier": "GNATStudio"})

# Check the assignment of payload Ids
assert(p2.id == p1.id + 1)

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
assert(len(result["elements"]) == 2)
m.close()
assert(not m.is_alive())