# Test the logic of the LAL analysis and handling of
# the association of CodeElements with subprogram nodes.

from achord.lal_analysis import UnitAnalyser
from achord.code_elements import CodeElement, SYNC_UNKNOWN, SYNC_CONNECTED, SYNC_ORPHANED
import libadalang as lal

import sys

workdir = sys.argv[1]

base = """package Traffic_Lights is
   
   type Light_Mode is (Green, Amber, Red, Red_And_Amber);
   
   type Light is private;
 
   procedure Set_Mode (L : Light; M : Light_Mode);
   
   function Get_Mode (L : Light) return Light_Mode;
   
private
   
   type Light is record
      Mode : Light_Mode := Red;
   end record;
   
end Traffic_Lights;
"""

after_modifications = """package Traffic_Lights is

-- a
-- b
-- c
-- d



   type Light_Mode is (Green, Amber, Red, Red_And_Amber);
   type Light is private;
 
   function Get_Mode 
      (L    : Light) 
      return Light_Mode;
   procedure Set_Mode 
      (L    : Light; 
       Mode : Light_Mode);
   
private
   
   type Light is record
      Mode : Light_Mode := Red;
   end record;
   
end Traffic_Lights;
"""

ctx = lal.AnalysisContext()
unit = ctx.get_from_buffer("traffic_lights.ads", base)

# Analyse all subprograms in ua
ua = UnitAnalyser(unit)

# Create a CodeElement for each subprogram
elements = []
for sha1 in ua.identified_subprograms:
    subp = ua.identified_subprograms[sha1]
    elements.append(CodeElement("traffic_lights.ads", subp.line, subp.sha1))

# now parse the code after "user modifications"

unit = ctx.get_from_buffer("traffic_lights.ads", after_modifications)
ua2 = UnitAnalyser(unit)
ua2.map_elements(elements)

# we're expecting one element "orphaned" and one "connected"
actual = {
    SYNC_UNKNOWN: 0,
    SYNC_ORPHANED: 0,
    SYNC_CONNECTED: 0
}
for e in elements:
    actual[e.sync_status] += 1

expected = {
    SYNC_UNKNOWN: 0,
    SYNC_ORPHANED: 1,
    SYNC_CONNECTED: 1
}
assert(actual == expected)
print("SUCCESS")
