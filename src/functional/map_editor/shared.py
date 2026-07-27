""" The chat rule, the zombies element subset and the SNBT formatting helpers. """
# Imports
from typing import Any, cast

from stewbeet import JsonDict

from ..map_editor_defs import ALL_ELEMENTS, ElementDef

# Constants
SEP: str = '{"text":"============================================","color":"dark_gray"}'
""" The horizontal rule every editor chat panel is framed with. """
ZB_ELEMENTS: dict[str, ElementDef] = {etype: einfo for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "zb_object"}
""" The zombies elements, which share one placement handler and one compound layout in storage. """

# Functions
def snbt_suggest(val: Any) -> str:
	""" Format a Python value as the SNBT a suggested command would carry.

	Args:
		val (Any): The value to format.
	Returns:
		str: Its SNBT spelling, quoted and suffixed the way Minecraft expects.

	Examples:
		>>> snbt_suggest([1, True, "a"])
		'[1,1b,"a"]'
	"""
	if isinstance(val, bool):
		return "1b" if val else "0b"
	elif isinstance(val, int):
		return str(val)
	elif isinstance(val, float):
		return f"{val}f"
	elif isinstance(val, str):
		return f'"{val}"'
	elif isinstance(val, list):
		return "[" + ",".join(snbt_suggest(v) for v in cast(list[Any], val)) + "]"
	elif isinstance(val, dict):
		return "{" + ",".join(f"{k}:{snbt_suggest(v)}" for k, v in cast(dict[str, Any], val).items()) + "}"
	return str(val)

def snbt_compound(d: JsonDict) -> str:
	""" Convert a dict to an SNBT compound string.

	Args:
		d (JsonDict): The compound's fields.
	Returns:
		str: The compound, braces included.

	Examples:
		>>> snbt_compound({"a": 1, "b": "x"})
		'{a:1,b:"x"}'
	"""
	return "{" + ",".join(f"{k}:{snbt_suggest(v)}" for k, v in d.items()) + "}"

