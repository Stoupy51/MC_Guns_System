""" Cheap NBT reads: bounce the value through a light entity instead of serializing a heavy one.

`data ... from entity <target>` has no fast path, it serializes the whole entity and only then walks
the path. A player drags its inventory, ender chest and entire recipe book along, measured at 886 us
against 110 us through a display, and a mob still drags its attributes, effects and equipment.
"""
# Imports
from stewbeet import Mem, write_versioned_function


# Classes
class Probe:
	""" Builders for the two bounce reads, plus the marker function they rely on. """

	ITEM_DISPLAY: str = "B5-0-0-0-3"
	""" Bookshelf's forceloaded item_display, created by bs.block and five other modules the pack ships. """

	POS_PATH: str = "_probe_pos"
	""" Path in {ns}:temp where Probe.pos leaves the three doubles. """

	@staticmethod
	def write_functions() -> None:
		""" Emit the marker body that Probe.pos summons. """
		ns: str = Mem.ctx.project_id

		# A kill only takes effect at the end of the tick, so the marker is moved out of the world first,
		# otherwise any positional selector running later in the same tick would still find it.
		write_versioned_function("shared/probe_pos", f"""
data modify storage {ns}:temp {Probe.POS_PATH} set from entity @s Pos
tp @s ~ -1000000 ~
kill @s
""")

	@staticmethod
	def pos(target: str = "@s") -> str:
		""" One command leaving the target position in {ns}:temp _probe_pos, as a list of three doubles.

		Args:
			target (str): Selector to read the position of
		Returns:
			str: The command to inline in a function body
		"""
		return f"execute at {target} summon minecraft:marker run function {Mem.ctx.project_id}:v{Mem.ctx.project_version}/shared/probe_pos"

	@staticmethod
	def item(slot: str, target: str = "@s") -> str:
		""" One command loading a target inventory slot into the shared item_display.

		Read the stack back with `from entity {Probe.ITEM_DISPLAY} item`, which carries no Slot key.

		Args:
			slot   (str): Slot name, ex: "weapon.mainhand" or "hotbar.1"
			target (str): Selector holding the stack
		Returns:
			str: The command to inline in a function body
		Examples:
			>>> Probe.item("hotbar.1")
			'item replace entity B5-0-0-0-3 contents from entity @s hotbar.1'
		"""
		return f"item replace entity {Probe.ITEM_DISPLAY} contents from entity {target} {slot}"

