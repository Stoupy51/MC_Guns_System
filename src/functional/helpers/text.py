""" Building text components: gradients, and splitting an emoji off a coloured label. """
# Imports
import re
from typing import Any

from stouputils.typing import JsonDict


# Classes
class Text:
	""" Building text components: gradients, and splitting an emoji off a coloured label. """

	# Functions
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

