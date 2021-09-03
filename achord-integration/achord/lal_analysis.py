"""This package contains the libadalang routines for
   analysing compilation units for the needs of the Achord
   integration
"""

import libadalang as lal
import re
import hashlib

whitespaces = re.compile("\s+")

class SubpDecl(object):

    def __init__(self, line, column, orig_text):
        """A subprogram decl. orig_text is the full text of the profile, encoded in utf-8"""
        self.line = line
        self.column = column
        self.orig_text = orig_text
        
        # Make an invariant hash of the profile spec

        # Replace any sequence of whitespaces/tabs/new lines with one space...
        condensed_text = re.sub(pat, " ", orig_text)

        # ... and produce a hash of that.
        self.sha1 = hashlib.sha1(condensed_text.encode("utf-8")).hexdigest()

class Unit_Analyser(object):

    def __init__(self, unit):
        """unit is a Libadalang AnalysisUnit"""

        # Note: do not store unit, it is not guaranteed to remain
        # valid. Instead, compute the necessary information
        # immediately.

        # Only process specs
        if not unit.root.p_unit_kind == "unit_specification":
            return

        # Find all subprogram units
        subpdecls = unit.root.findall(lal.SubpDecl)
        for subpdecl in subpdecls:
            start_line = subpdecl.sloc_range.start.line
            start_column = subpdecl.sloc_range.start.column
            orig_text = subpdecl.text

