""" The chat rule, the zombies element subset, and the help shown in the editor's dialog forms. """
# Imports
from collections.abc import Sequence

from stewbeet import JsonDict

from ..helpers.text import Text
from ..map_editor_defs import ALL_ELEMENTS, FIELD_DOCS, ElementDef

# Constants
SEP: str = '{"text":"============================================","color":"dark_gray"}'
""" The horizontal rule every editor chat panel is framed with. """
ZB_ELEMENTS: dict[str, ElementDef] = {etype: einfo for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "zb_object"}
""" The zombies elements, which share one placement handler and one compound layout in storage. """
GROUP_ID_ELEMENTS: tuple[str, ...] = ("zombie_spawn", "player_spawn_zb", "special_spawn")
""" The only elements carrying a group_id, the spawn group a door opens.
A door's link_id is its front-room group and back_group_id its back room; nothing else reads one. """
AXIOM_KEYS: tuple[str, ...] = ("name", "min", "max")
""" Marker data Axiom reads, to label a marker and to draw the box between two corners: written by the editor, never saved.
An element's own `name` field is kept under `title` while it is a marker. """


# Functions
def help_legend(fields: Sequence[tuple[str, tuple[str, str] | str]]) -> JsonDict:
	""" A dialog body of "ⓘ" chips, one per field label, five a line, each showing its FIELD_DOCS entry on hover.

	Only text inputs show a tooltip on their own label: sliders, option buttons and check boxes do not.
	"""
	contents: list[str | JsonDict] = ["", {"text": "Hover a name for its help:", "color": "gray"}]
	for i, (label, doc) in enumerate(fields):
		contents += ["\n" if i % 5 == 0 else "   ", {"text": f"ⓘ {label}", "color": "aqua", "hover_event": doc_hover(doc)}]
	return {"type": "minecraft:plain_message", "width": 400, "contents": contents}


def doc_hover(doc: tuple[str, str] | str) -> JsonDict:
	""" A hover event showing a FIELD_DOCS entry. """
	return {"action": "show_text", "value": Text.help(FIELD_DOCS[doc])}

