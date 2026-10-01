""" Building text components: gradients, splitting an emoji off a coloured label, and naming a player. """
# Imports
import re

from stouputils.typing import JsonDict


# Classes
class Text:
	""" Building text components: gradients, splitting an emoji off a coloured label, and naming a player. """

	# Functions
	@staticmethod
	def player(ns: str, selector: str = "@s", side: str = "mp", **style: str) -> str:
		""" A player's name with their level in front of it, as one grouped component.

		The leading `""` keeps the group from inheriting the first element's styling.
		`selector` must match one entity, and an unset level renders as `[]` (`progression/tick_player` sets it).

		Args:
			selector: Single-entity selector, ex: "@s" or "@a[tag=mgs.temp_killer]".
			side: "mp" or "zb", which of the two independent levels to show.
			**style: SNBT attributes applied to the NAME only, ex: color="yellow", bold="true".

		>>> Text.player("mgs", "@s").startswith('["",{"text":"[","color":"dark_gray"}')
		True
		>>> '{"selector":"@s","bold":true}' in Text.player("mgs", "@s", bold="true")
		True
		"""
		# Booleans stay unquoted, matching styled_text: "bold":"true" is a string, which SNBT rejects.
		attrs: str = "".join(
			f',"{key}":{value}' if value in ("true", "false") else f',"{key}":"{value}"'
			for key, value in style.items()
		)
		return (
			f'["",{{"text":"[","color":"dark_gray"}}'
			f',{{"score":{{"name":"{selector}","objective":"{ns}.{side}.xp_level"}},"color":"gold"}}'
			f',{{"text":"] ","color":"dark_gray"}}'
			f',{{"selector":"{selector}"{attrs}}}]'
		)

	@staticmethod
	def styled_text(text: str, **attrs: str) -> str:
		""" Create a styled text component, automatically splitting non-alphanumeric
		prefixes/suffixes into raw strings so the lang plugin only sees clean alpha text
		and emojis are NOT tinted by the style (emojis always render with default color).

		Args:
			text: The text to display (may contain leading/trailing emoji/symbols).
			**attrs: SNBT attributes like color, bold, italic.

		Returns:
			str: SNBT text component (single object or list with a neutral head).
		"""
		m = re.match(r'^([^a-zA-Z0-9]*)(.*?)([^a-zA-Z0-9]*)$', text, re.DOTALL)
		prefix, alpha, suffix = m.groups() if m else ("", text, "")

		attr_str = ",".join(f'{k}:"{v}"' if v not in ("true", "false") else f'{k}:{v}' for k, v in attrs.items())

		if not prefix and not suffix:
			return f'{{text:"{alpha}",{attr_str}}}' if attr_str else f'{{text:"{alpha}"}}'

		# A neutral head, so the emoji prefix and suffix stay uncoloured.
		parts = ['""']
		if prefix:
			parts.append(f'"{prefix}"')
		if alpha:
			parts.append(f'{{text:"{alpha}",{attr_str}}}' if attr_str else f'{{text:"{alpha}"}}')
		if suffix:
			parts.append(f'"{suffix}"')
		return f'[{",".join(parts)}]'

	@staticmethod
	def split_emoji(text: str, **style: str | bool) -> JsonDict | list[str | JsonDict]:
		""" Build a (Python) text component where any non-alphanumeric prefix/suffix (emojis)
		renders uncolored/unstyled, while the alphanumeric core keeps the given style.

		Args:
			text: The text to display (may contain leading/trailing emoji/symbols).
			**style: Component attributes like color or bold.

		Returns:
			JsonDict | list: A single styled component, or a list with a neutral head.
		"""
		m = re.match(r'^([^a-zA-Z0-9]*)(.*?)([^a-zA-Z0-9]*)$', text, re.DOTALL)
		prefix, alpha, suffix = m.groups() if m else ("", text, "")
		if not alpha or (not prefix and not suffix):
			return {"text": text, **style}
		parts: list[str | JsonDict] = [""]
		if prefix:
			parts.append(prefix)
		parts.append({"text": alpha, **style} if style else {"text": alpha})
		if suffix:
			parts.append(suffix)
		return parts

