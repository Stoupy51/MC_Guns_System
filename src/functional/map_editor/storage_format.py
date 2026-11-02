""" How a zombies map is kept in storage: written small by the editor's save, read back whole by `maps/inflate`.

An element leaves out every field holding its `ElementDef.defaults` value, and keeps its yaw as whole degrees, left out at 0:
`{pos:[-46,-21,5],yaw:90,perk_id:"stamin_up"}`. Only spawns keep a group_id, left out at 0.
A map writes the `shared_fields` of a kind once, under `shared.<etype>`, from the first element saved; the others leave out the same values.
Doors are grouped by link, each block keeping its own block id and yaw only when they differ from its link's:
`{link_id:2,name:"Parking",price:750,block:"minecraft:waxed_copper_bars",yaw:180,blocks:[{pos:[-8,-7,2]},{pos:[3,-6,12],block:"minecraft:oak_planks",yaw:0}]}`.

`maps/inflate` turns the map in `{ns}:temp _inf_map` back into what the game and the editor read: one compound per element, every field set,
and `rotation:[yaw,pitch]` in place of yaw. An element still holding a rotation, a door without blocks and a `barriers` list (the older name of `barricades`) are read as they are, the defaults they lack aside.
"""
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.snbt import snbt
from ..map_editor_defs import ElementDef
from .shared import GROUP_ID_ELEMENTS, ZB_ELEMENTS

# Constants
DOOR_LINK_KEYS: tuple[str, ...] = ("link_id", "block")
""" Door fields always written on its link: the one it is grouped by, and the one its blocks compare theirs to. """
MAX_COMMANDS: int = 262144
""" Four times the vanilla max_command_sequence_length: saving or loading a big map runs tens of thousands of commands in one call. """


# Functions
def write_storage_format() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
execute store result score #max_commands {ns}.data run gamerule max_command_sequence_length
execute if score #max_commands {ns}.data matches ..{MAX_COMMANDS - 1} run gamerule max_command_sequence_length {MAX_COMMANDS}

# Whole maps an older version of the pack left behind in temp storage, each now removed right after use.
{"\n".join(f"data remove storage {ns}:temp {key}" for key in ("map_load", "_map_entry", "_lb_view", "map_menu", "_export", "_dup", "_inf_map"))}
""")

	for etype, einfo in ZB_ELEMENTS.items():
		write_versioned_function(f"maps/compact/{etype}", compact_lines(ns, version, etype, einfo))
	write_door_links(ns, version)

	write_versioned_function("maps/inflate", "\n\n".join([
		f"""# Run with a zombies map in {ns}:temp _inf_map.
data modify storage {ns}:temp _inf_shared set value {{}}
data modify storage {ns}:temp _inf_shared set from storage {ns}:temp _inf_map.shared
data remove storage {ns}:temp _inf_map.shared
execute unless data storage {ns}:temp _inf_map.barricades run data modify storage {ns}:temp _inf_map.barricades set from storage {ns}:temp _inf_map.barriers
data remove storage {ns}:temp _inf_map.barriers""",
		*(f"""data modify storage {ns}:temp _inf_src set value []
data modify storage {ns}:temp _inf_src set from storage {ns}:temp _inf_map.{einfo.save_path}
execute if data storage {ns}:temp _inf_src[0] run data modify storage {ns}:temp _inf_map.{einfo.save_path} set value []
execute if data storage {ns}:temp _inf_src[0] run function {ns}:v{version}/maps/inflate/{etype}""" for etype, einfo in ZB_ELEMENTS.items()),
	]))
	for etype, einfo in ZB_ELEMENTS.items():
		write_versioned_function(f"maps/inflate/{etype}_fields", inflate_field_lines(ns, version, etype, einfo))
		if etype != "door":
			write_versioned_function(f"maps/inflate/{etype}", f"""
data modify storage {ns}:temp _inf set from storage {ns}:temp _inf_src[0]
function {ns}:v{version}/maps/inflate/{etype}_fields
data modify storage {ns}:temp _inf_map.{einfo.save_path} append from storage {ns}:temp _inf
data remove storage {ns}:temp _inf_src[0]
execute if data storage {ns}:temp _inf_src[0] run function {ns}:v{version}/maps/inflate/{etype}
""")
	write_door_inflate(ns, version)

	write_versioned_function("maps/inflate/rotation", f"""
execute if data storage {ns}:temp _inf.rotation run return 0
data modify storage {ns}:temp _inf.rotation set value [0.0f,0.0f]
execute store result storage {ns}:temp _inf.rotation[0] float 1 run data get storage {ns}:temp _inf.yaw
execute if data storage {ns}:temp _inf.pitch run data modify storage {ns}:temp _inf.rotation[1] set from storage {ns}:temp _inf.pitch
data remove storage {ns}:temp _inf.yaw
""")


def compact_lines(ns: str, version: str, etype: str, einfo: ElementDef) -> str:
	""" Body of maps/compact/<etype>, run as a marker being saved with its entry in `{ns}:temp _save_zb`: what the entry leaves out, then where it goes. """
	group_id: str = (
		f"execute if data storage {ns}:temp _save_zb{{group_id:0}} run data remove storage {ns}:temp _save_zb.group_id"
		if etype in GROUP_ID_ELEMENTS else f"data remove storage {ns}:temp _save_zb.group_id"
	)
	shared: str = f"{ns}:temp map_edit.map.shared.{etype}"
	kept: tuple[str, ...] = (*einfo.shared_fields, *(DOOR_LINK_KEYS if etype == "door" else ()))
	return "\n".join([
		group_id,
		*([] if einfo.has_rotation else [f"data remove storage {ns}:temp _save_zb.yaw"]),
		*(
			f"execute unless data storage {shared}.{field} run data modify storage {shared}.{field} set from storage {ns}:temp _save_zb.{field}\n"
			+ strip_unless_differs(ns, field, f"set from storage {shared}.{field}")
			for field in einfo.shared_fields
		),
		*(strip_default(ns, field, default) for field, default in einfo.defaults.items() if field not in kept),
		f"function {ns}:v{version}/maps/compact/door_block" if etype == "door"
		else f"data modify storage {ns}:temp map_edit.map.{einfo.save_path} append from storage {ns}:temp _save_zb",
	])


def strip_default(ns: str, field: str, default: object) -> str:
	""" The commands leaving `field` out of `{ns}:temp _save_zb` while it holds `default`.

	An NBT pattern also matches a compound or a non-empty list that merely contains it, so those are compared whole.

	>>> strip_default("mgs", "price", 1000)
	'execute if data storage mgs:temp _save_zb{price:1000} run data remove storage mgs:temp _save_zb.price'
	>>> strip_default("mgs", "mob", {"entity": "zombie"}).splitlines()[2]
	'execute store success score #differs mgs.data run data modify storage mgs:temp _cmp set value {entity:"zombie"}'
	"""
	value: str = snbt(default)
	if not isinstance(default, dict | list) or value == "[]":
		return f"execute if data storage {ns}:temp _save_zb{{{field}:{value}}} run data remove storage {ns}:temp _save_zb.{field}"
	return strip_unless_differs(ns, field, f"set value {value}")


def strip_unless_differs(ns: str, field: str, modify: str) -> str:
	""" The commands leaving `field` out of `{ns}:temp _save_zb` when `data modify` with `modify` would not change it. """
	return f"""data remove storage {ns}:temp _cmp
data modify storage {ns}:temp _cmp set from storage {ns}:temp _save_zb.{field}
execute store success score #differs {ns}.data run data modify storage {ns}:temp _cmp {modify}
execute if score #differs {ns}.data matches 0 run data remove storage {ns}:temp _save_zb.{field}"""


def write_door_links(ns: str, version: str) -> None:
	""" Write the save of one door block into its link's entry, which the link's first door saved creates. """
	compact: str = f"{ns}:v{version}/maps/compact"
	link: str = f"{ns}:temp map_edit.map.doors[{{link_id:$(link_id)}}]"

	write_versioned_function("maps/compact/door_block", f"""
data modify storage {ns}:temp _door_block set value {{}}
data modify storage {ns}:temp _door_block.pos set from storage {ns}:temp _save_zb.pos
data remove storage {ns}:temp _save_zb.pos
function {compact}/door_link with storage {ns}:temp _save_zb
""")

	differs_warning: str = (
		f'[{MGS_TAG},{{"text":"⚠ The door at ","color":"yellow"}},{{"entity":"@s","nbt":"Pos","color":"white"}},'
		f'{{"text":" differs from the rest of link ","color":"yellow"}},{{"storage":"{ns}:temp","nbt":"_save_zb.link_id","color":"white"}},'
		f'{{"text":", which keeps the values of one of its doors. The ✎ buttons of a door set its whole link.","color":"yellow"}}]'
	)
	## Macro (link_id), run as the door marker.
	write_versioned_function("maps/compact/door_link", f"""
$execute unless data storage {link} run function {compact}/door_new
$data modify storage {ns}:temp _door_link set from storage {link}

data remove storage {ns}:temp _cmp
data modify storage {ns}:temp _cmp set from storage {ns}:temp _save_zb.block
execute store success score #differs {ns}.data run data modify storage {ns}:temp _cmp set from storage {ns}:temp _door_link.block
execute if score #differs {ns}.data matches 1 run data modify storage {ns}:temp _door_block.block set from storage {ns}:temp _save_zb.block
execute store result score #link_yaw {ns}.data run data get storage {ns}:temp _door_link.yaw
execute unless score #yaw {ns}.data = #link_yaw {ns}.data store result storage {ns}:temp _door_block.yaw int 1 run scoreboard players get #yaw {ns}.data
$data modify storage {link}.blocks append from storage {ns}:temp _door_block

data remove storage {ns}:temp _door_link.blocks
data remove storage {ns}:temp _door_link.block
data remove storage {ns}:temp _door_link.yaw
data remove storage {ns}:temp _save_zb.block
data remove storage {ns}:temp _save_zb.yaw
execute store success score #differs {ns}.data run data modify storage {ns}:temp _door_link set from storage {ns}:temp _save_zb
execute if score #differs {ns}.data matches 1 run tellraw @a[tag={ns}.map_editor] {differs_warning}
""")

	write_versioned_function("maps/compact/door_new", f"""
data modify storage {ns}:temp _door_new set from storage {ns}:temp _save_zb
data modify storage {ns}:temp _door_new.blocks set value []
data modify storage {ns}:temp map_edit.map.doors append from storage {ns}:temp _door_new
""")


def inflate_field_lines(ns: str, version: str, etype: str, einfo: ElementDef) -> str:
	""" Body of maps/inflate/<etype>_fields, giving the element in `{ns}:temp _inf` its rotation and every field it leaves out. """
	entry: str = f"{ns}:temp _inf"
	upgrades: list[str] = [
		f"execute if data storage {entry}.{field}.Name run data modify storage {entry}.{field}.id set from storage {entry}.{field}.Name\n"
		f"execute if data storage {entry}.{field}.Properties run data modify storage {entry}.{field}.properties set from storage {entry}.{field}.Properties\n"
		f"data remove storage {entry}.{field}.Name\n"
		f"data remove storage {entry}.{field}.Properties\n"
		f"execute unless data storage {entry}.{field} run data modify storage {entry}.{field} set from storage {ns}:temp _inf_shared.{etype}.{field}"
		for field in einfo.shared_fields
	]
	return "\n".join([
		f"function {ns}:v{version}/maps/inflate/rotation",
		*upgrades,
		*(f"execute unless data storage {entry}.{field} run data modify storage {entry}.{field} set value {snbt(default)}" for field, default in einfo.defaults.items()),
		*([f"execute unless data storage {entry}.group_id run data modify storage {entry}.group_id set value 0"] if etype in GROUP_ID_ELEMENTS else []),
	])


def write_door_inflate(ns: str, version: str) -> None:
	""" Write maps/inflate/door, turning each link back into one entry per door block. """
	inflate: str = f"{ns}:v{version}/maps/inflate"
	write_versioned_function("maps/inflate/door", f"""
data modify storage {ns}:temp _inf_link set from storage {ns}:temp _inf_src[0]
data modify storage {ns}:temp _inf_blocks set value []
data modify storage {ns}:temp _inf_blocks set from storage {ns}:temp _inf_link.blocks

# A door saved without blocks is a link of its own block.
execute unless data storage {ns}:temp _inf_link.blocks run data modify storage {ns}:temp _inf_blocks append value {{}}
data remove storage {ns}:temp _inf_link.blocks
execute if data storage {ns}:temp _inf_blocks[0] run function {inflate}/door_block

data remove storage {ns}:temp _inf_src[0]
execute if data storage {ns}:temp _inf_src[0] run function {inflate}/door
""")
	write_versioned_function("maps/inflate/door_block", f"""
data modify storage {ns}:temp _inf set from storage {ns}:temp _inf_link
data modify storage {ns}:temp _inf merge from storage {ns}:temp _inf_blocks[0]
function {inflate}/door_fields
data modify storage {ns}:temp _inf_map.doors append from storage {ns}:temp _inf
data remove storage {ns}:temp _inf_blocks[0]
execute if data storage {ns}:temp _inf_blocks[0] run function {inflate}/door_block
""")

