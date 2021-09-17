"""Contains the editor actions"""

import GPS

from achord.lal_analysis import UnitAnalyser
from achord.project_support import make_path_project_relative
from achord.achord_connection import get_achord_elements

# TODO: connect styles to preferences
unassociated_entity_style = GPS.Style("unassociated_entity")
unassociated_entity_style.set_background("#ffff00")
associated_entity_style = GPS.Style("associated_entity")
associated_entity_style.set_background("#00ff00")

CATEGORY = "Achord"


def open_element_info_dialog(message):
    GPS.Console().write(f"{message.subp}\n")


def decorate_editor(buffer):
    unit = buffer.get_analysis_unit()

    if not unit.root.p_unit_kind == "unit_specification":
        return

    file = buffer.file()
    relname = make_path_project_relative(file.name())

    # Process the editor
    ua = UnitAnalyser(unit)

    # Map all the elements
    els = get_achord_elements()
    ua.map_elements(els)

    # Remove existing messages
    for m in GPS.Message.list(category=CATEGORY, file=file):
        m.remove()

    # Create a message for each element
    for id in ua.identified_subprograms:
        subp = ua.identified_subprograms[id]
        m = GPS.Message(
            category=CATEGORY,
            file=buffer.file(),
            line=subp.line,
            column=subp.column,
            text="",
            show_on_editor_side=True,
            show_in_locations=False,
            auto_jump_to_first=False,
        )
        if subp.connected_element is None:
            m.set_style(unassociated_entity_style)
            m.subp = subp
            m.set_subprogram(open_element_info_dialog, "gps-compile-symbolic", "")
        else:
            m.set_style(associated_entity_style)
