""" Python values written as the SNBT a command carries. """
# Imports
from typing import cast

from stewbeet import JsonDict
from stouputils.typing import JsonList


# Functions
def snbt(value: object) -> str:
	""" Format a Python value as SNBT, quoted and suffixed the way Minecraft expects.

	>>> snbt({"a": [1, True, "x"], "b": 0.5})
	'{a:[1,1b,"x"],b:0.5f}'
	"""
	if isinstance(value, bool):
		return "1b" if value else "0b"
	if isinstance(value, int):
		return str(value)
	if isinstance(value, float):
		return f"{value}f"
	if isinstance(value, str):
		return f'"{value}"'
	if isinstance(value, list):
		return "[" + ",".join(snbt(v) for v in cast(JsonList, value)) + "]"
	if isinstance(value, dict):
		return "{" + ",".join(f"{k}:{snbt(v)}" for k, v in cast(JsonDict, value).items()) + "}"
	return str(value)

