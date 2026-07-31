""" The look of a planted bomb, and naming the site it went down on.

Both bomb modes put the same object on the same kind of site, so the entity trio and the per-letter chat
announce live here rather than being typed twice with a drifting Y offset.
"""
# ruff: noqa: E501
# Imports
from ....helpers import MGS_TAG
from ..base import GameModeVariant

# Constants
SITE_LETTERS: tuple[str, ...] = ("A", "B", "C", "D")
""" The letters `BombSites.write_summoning` can hand out, in order. """
TNT_LIFT: float = 0.625
""" How far up the half-scale TNT sits inside the site's chest.
A chest is 0.875 tall and the model is 0.5, so 0.625 leaves exactly half of it above the lid: buried at
0.0 it was invisible, and floating clear of the block looked like it was not attached to anything. """


# Classes
class BombVisuals:
	""" Entity trios and chat announces for a planted bomb. """

	# Functions
	@staticmethod
	def planted_entities(ns: str, marker_tag: str, vis_tag: str, hud_tag: str, label: str) -> str:
		""" Return the three summons making up a planted bomb, at the current position.

		Args:
			ns         (str): Project namespace.
			marker_tag (str): Tag of the logical marker every gameplay check selects.
			vis_tag    (str): Tag of the TNT block_display.
			hud_tag    (str): Tag of the countdown text_display.
			label      (str): Text the countdown starts on, before the first per-second rewrite.
		Returns:
			str: Three summon commands, one per line.
		"""
		return f"""summon minecraft:marker ~ ~ ~ {{Tags:["{ns}.{marker_tag}","{ns}.gm_entity"]}}
summon minecraft:block_display ~ ~ ~ {{Tags:["{ns}.{vis_tag}","{ns}.gm_entity"],block_state:{{Name:"minecraft:tnt"}},transformation:{{translation:[-0.25f,{TNT_LIFT}f,-0.25f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[0.5f,0.5f,0.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}}}}
summon minecraft:text_display ~ ~ ~ {{Tags:["{ns}.{hud_tag}","{ns}.gm_entity"],billboard:"vertical",text:[{{"text":"💣 {label}","color":"red","bold":true}}],transformation:{{translation:[0.0f,1.4f,0.0f],left_rotation:[0.0f,0.0f,0.0f,1.0f],scale:[1.5f,1.5f,1.5f],right_rotation:[0.0f,0.0f,0.0f,1.0f]}},shadow:true,see_through:true}}"""

	@staticmethod
	def announce_site_lines(variant: GameModeVariant, message: str, generic: str = "", color: str = "red") -> str:
		""" Return one `tellraw` per site letter, selected by the `<key>_site_<letter>` tag on `@s`.

		Naming the site is how the defending side knows which one to rotate to, so it is worth a line
		per letter rather than a generic "the bomb was planted".

		Args:
			variant (GameModeVariant): The mode whose site tags are being tested.
			message (str):             Announce text, with `{{letter}}` where the letter goes.
			generic (str):             Text for a site carrying no letter tag (Demolition's overtime site).
				Omit to emit no fallback line at all.
			color   (str):             Colour of the announce.
		Returns:
			str: One command per letter in SITE_LETTERS, plus the fallback when `generic` is given.
		"""
		ns, key = variant.ns, variant.key
		lines: list[str] = [
			f'execute if entity @s[tag={ns}.{key}_site_{letter}] run tellraw @a [{MGS_TAG},"💣 ",{{"text":"{message.format(letter=letter)}","color":"{color}","bold":true}}]'
			for letter in SITE_LETTERS
		]
		if generic:
			no_letter: str = " ".join(f"unless entity @s[tag={ns}.{key}_site_{letter}]" for letter in SITE_LETTERS)
			lines.append(f'execute {no_letter} run tellraw @a [{MGS_TAG},"💣 ",{{"text":"{generic}","color":"{color}","bold":true}}]')
		return "\n".join(lines)
