""" Editor markers and displays that outlive their session, and markers saved twice.

A session's entities only die where their chunks are loaded when it closes. Every entity of the editor takes the
current session's number within a second of appearing, and one holding an older number dies as soon as it loads again.
"""
# Imports
from stewbeet import Mem, write_load_file, write_tick_file, write_versioned_function

from ..helpers import MGS_TAG
from ..map_editor_defs import ALL_ELEMENTS


# Functions
def write_editor_leftovers() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	editor: str = f"{ns}:v{version}/maps/editor"

	write_load_file(f"""
scoreboard objectives add {ns}.ed.session dummy
scoreboard players add #ed_session {ns}.data 0
""")

	write_tick_file(f"""
scoreboard players operation #ed_sweep {ns}.data = #total_tick {ns}.data
scoreboard players operation #ed_sweep {ns}.data %= #20 {ns}.data
execute if score #ed_sweep {ns}.data matches 0 run function {editor}/sweep
""")
	write_versioned_function("maps/editor/sweep", f"""
execute as @e[type=minecraft:marker,tag={ns}.map_element] run function {editor}/session_check
execute as @e[type=minecraft:item_display,tag={ns}.editor_display] run function {editor}/session_check
execute as @e[type=minecraft:block_display,tag={ns}.editor_display] run function {editor}/session_check
""")
	write_versioned_function("maps/editor/session_check", f"""
execute unless score @s {ns}.ed.session matches -2147483648.. run return run scoreboard players operation @s {ns}.ed.session = #ed_session {ns}.data
execute unless score @s {ns}.ed.session = #ed_session {ns}.data run kill @s
""")

	## Run as the editor entering or leaving: a session starts with its first editor and ends with its last.
	write_versioned_function("maps/editor/next_session", f"""
execute unless entity @a[scores={{{ns}.mp.map_edit=1}}] run scoreboard players add #ed_session {ns}.data 1
""")

	write_duplicates(ns, editor)


def write_duplicates(ns: str, editor: str) -> None:
	""" Write maps/editor/remove_duplicates, killing every marker of a kind that has the same block and data as another one. """
	kinds: list[str] = [etype for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type not in ("base", "config")]
	for etype in kinds:
		same_kind: str = f"@e[type=minecraft:marker,tag={ns}.element.{etype},tag=!{ns}.ed_keep,distance=..0.01]"
		write_versioned_function(f"maps/editor/dedupe/{etype}", f"""
execute if entity @s[tag={ns}.ed_dup] run return 0
tag @s add {ns}.ed_keep
execute unless entity {same_kind} run return 0
function {editor}/dedupe_read
execute as {same_kind} run function {editor}/dedupe_same
""")

	write_versioned_function("maps/editor/dedupe_read", f"""
data modify storage {ns}:temp _dedupe set from entity @s data
data remove storage {ns}:temp _dedupe._ed
data remove storage {ns}:temp _dedupe._disp_sig
""")
	# Several spawns on one block with different mobs are meant: only an exact copy goes.
	write_versioned_function("maps/editor/dedupe_same", f"""
data modify storage {ns}:temp _dedupe_other set from entity @s data
data remove storage {ns}:temp _dedupe_other._ed
data remove storage {ns}:temp _dedupe_other._disp_sig
execute store success score #differs {ns}.data run data modify storage {ns}:temp _dedupe_other set from storage {ns}:temp _dedupe
execute if score #differs {ns}.data matches 0 run tag @s add {ns}.ed_dup
""")

	write_versioned_function("maps/editor/remove_duplicates", "\n".join([
		*(f"execute as @e[type=minecraft:marker,tag={ns}.element.{etype}] at @s run function {editor}/dedupe/{etype}" for etype in kinds),
		f"tag @e[type=minecraft:marker,tag={ns}.ed_keep] remove {ns}.ed_keep",
		f"execute store result score #ed_dups {ns}.data run kill @e[type=minecraft:marker,tag={ns}.ed_dup]",
		f'execute if score #ed_dups {ns}.data matches 1.. run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"score":{{"name":"#ed_dups","objective":"{ns}.data"}},"color":"white"}},{{"text":" duplicate elements removed (same kind, block and values).","color":"yellow"}}]',
	]))

