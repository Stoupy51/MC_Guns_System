""" Building text components: gradients, splitting an emoji off a coloured label, and naming a player. """
# Imports
import re
from typing import Any

from stouputils.typing import JsonDict


# Classes
class Text:
	""" Building text components: gradients, splitting an emoji off a coloured label, and naming a player. """

	# Functions
	@staticmethod
	def player(ns: str, selector: str = "@s", side: str = "mp", **style: str) -> str:
		""" A player's name with their level in front of it, as one grouped component.

		Returned as a bracketed list rather than a bare comma-separated fragment so it can be dropped
		anywhere a single component is expected. The leading `""` keeps the group from inheriting the
		first element's styling.

		The `selector` has to resolve to exactly ONE entity, because a score component reads a single
		score — the same constraint `game/sidebar.py` already relies on for its FFA rank rows. A player
		whose level score is still unset renders as `[]`, which is why `progression/tick_player`
		initialises everyone within a second of joining.

		Args:
			ns       (str): Project namespace.
			selector (str): Single-entity selector, ex: "@s" or "@a[tag=mgs.temp_killer]".
			side     (str): "mp" or "zb" — which of the two independent levels to show.
			**style  (str): SNBT attributes applied to the NAME only, ex: color="yellow", bold="true".
		Returns:
			str: SNBT list component, ex: `["",{"text":"["...},{"score":...},{"text":"] "...},{"selector":"@s"}]`

		Examples:
			>>> Text.player("mgs", "@s").startswith('["",{"text":"[","color":"dark_gray"}')
			True
			>>> '"objective":"mgs.zb.xp_level"' in Text.player("mgs", "@s", side="zb")
			True
			>>> '{"selector":"@s","color":"red"}' in Text.player("mgs", "@s", color="red")
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
			text    (str): The text to display (may contain leading/trailing emoji/symbols).
			**attrs (str): SNBT attributes like color, bold, italic.

		Returns:
			str: SNBT text component (single object or list with a neutral head).
		"""
		# Check if text has non-alphanumeric content (besides spaces)
		m = re.match(r'^([^a-zA-Z0-9]*)(.*?)([^a-zA-Z0-9]*)$', text, re.DOTALL)
		prefix, alpha, suffix = m.groups() if m else ("", text, "")

		# Build attributes string for SNBT
		attr_str = ",".join(f'{k}:"{v}"' if v not in ("true", "false") else f'{k}:{v}' for k, v in attrs.items())

		if not prefix and not suffix:
			# Pure alphanumeric - single component
			return f'{{text:"{alpha}",{attr_str}}}' if attr_str else f'{{text:"{alpha}"}}'

		# Build list: neutral head (so emoji prefix/suffix stay uncolored), styled alpha text
		parts = ['""']
		if prefix:
			parts.append(f'"{prefix}"')
		if alpha:
			parts.append(f'{{text:"{alpha}",{attr_str}}}' if attr_str else f'{{text:"{alpha}"}}')
		if suffix:
			parts.append(f'"{suffix}"')
		return f'[{",".join(parts)}]'

	@staticmethod
	def split_emoji(text: str, **style: str | bool) -> "JsonDict | list[Any]":
		""" Build a (Python) text component where any non-alphanumeric prefix/suffix (emojis)
		renders uncolored/unstyled, while the alphanumeric core keeps the given style.

		Args:
			text    (str): The text to display (may contain leading/trailing emoji/symbols).
			**style (str | bool): Component attributes like color or bold.

		Returns:
			JsonDict | list: A single styled component, or a list with a neutral head.
		"""
		m = re.match(r'^([^a-zA-Z0-9]*)(.*?)([^a-zA-Z0-9]*)$', text, re.DOTALL)
		prefix, alpha, suffix = m.groups() if m else ("", text, "")
		if not alpha or (not prefix and not suffix):
			# Pure alphanumeric or pure symbols: keep as a single styled component
			return {"text": text, **style}
		parts: list[Any] = ["", ]
		if prefix:
			parts.append(prefix)
		parts.append({"text": alpha, **style} if style else {"text": alpha})
		if suffix:
			parts.append(suffix)
		return parts

