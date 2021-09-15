"""This package contains the libadalang routines for
   analysing compilation units for the needs of the Achord
   integration
"""

import libadalang as lal
import re
import hashlib

from achord.project_support import make_path_project_relative
from achord.code_elements import SYNC_CONNECTED, SYNC_ORPHANED, CodeElement, SubpDecl

whitespaces = re.compile("\s+")


class UnitAnalyser(object):
    def __init__(self, unit):
        """unit is a Libadalang AnalysisUnit"""

        # Note: do not store unit, it is not guaranteed to remain
        # valid. Instead, compute the necessary information
        # immediately.

        self.project_relative_filename = make_path_project_relative(unit.filename)

        # Only process specs
        if not unit.root.p_unit_kind == "unit_specification":
            return

        # Find all subprogram units
        subpdecls = unit.root.findall(lal.SubpDecl)

        self.identified_subprograms = {}
        # Identified bits of code, indexed by sha1

        for subpdecl in subpdecls:
            start_line = subpdecl.sloc_range.start.line
            start_column = subpdecl.sloc_range.start.column
            orig_text = subpdecl.text

            s = SubpDecl(start_line, start_column, orig_text)
            self.identified_subprograms[s.sha1] = s

    def map_elements(self, element_list):
        """Look at all achord elements in elements_list, and set the
           "sync_status" field for all Code Elements matching this unit.
        """

        for el in element_list:
            # We're only interest in mapping CodeElements
            if not isinstance(el, CodeElement.__class__):
                continue

            if el.project_relative_filename == self.project_relative_filename:
                if el.sha1 in self.identified_subprograms:
                    el.sync_status = SYNC_CONNECTED
                    el.subp = self.identified_subprograms[el.sha1]
                    self.identified_subprograms[el.sha1].connect_element(el)
                else:
                    el.sync_status = SYNC_ORPHANED
