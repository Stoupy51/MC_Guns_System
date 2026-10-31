""" Removing the nearest marker, reporting what was destroyed, and the Revert button that brings it back. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import ALL_ELEMENTS


# Functions
def write_editor_destroy() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	editor: str = f"{ns}:v{version}/maps/editor"

	write_versioned_function("maps/editor/handle_destroy", f"""
# Within 3 blocks.
execute at @s unless entity @n[tag={ns}.map_element,distance=..3] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 3 blocks!","color":"red"}}]
execute at @s as @n[tag={ns}.map_element,distance=..3] run function {editor}/destroy_element

# So a destroyed machine's model disappears at once.
function {editor}/refresh_displays
""")

	write_versioned_function("maps/editor/destroy_element", f"""
# Run as the marker to destroy.
{element_lines(ns, "removed")}

# What Revert summons again, without the blocks the editor computes back from the rest. Each removal keeps its own entry, the last 32 of the session.
scoreboard players add #ed_removed_id {ns}.data 1
data modify storage {ns}:temp _ed_removed set value {{marker:{{}}}}
execute store result storage {ns}:temp _ed_removed.id int 1 run scoreboard players get #ed_removed_id {ns}.data
data modify storage {ns}:temp _ed_removed.marker.Pos set from entity @s Pos
data modify storage {ns}:temp _ed_removed.marker.Rotation set from entity @s Rotation
data modify storage {ns}:temp _ed_removed.marker.Tags set from entity @s Tags
data modify storage {ns}:temp _ed_removed.marker.data set from entity @s data
data remove storage {ns}:temp _ed_removed.marker.data._ed
data remove storage {ns}:temp _ed_removed.marker.data._disp_sig
data modify storage {ns}:temp map_edit.removed append from storage {ns}:temp _ed_removed
execute if data storage {ns}:temp map_edit.removed[32] run data remove storage {ns}:temp map_edit.removed[0]
function {editor}/removed_message with storage {ns}:temp _ed_removed

kill @s
""")
	revert_btn: str = Dialogs.btn("Revert", f"/function {editor}/revert {{id:$(id)}}", "green", "Put it back as it was", action="run_command")
	write_versioned_function("maps/editor/removed_message", f"""
$tellraw @a[tag={ns}.map_editor] ["  ",{revert_btn},"  ",{{"text":"Data: ","color":"gray"}},{{"storage":"{ns}:temp","nbt":"_ed_removed.marker.data","color":"white"}}]
""")

	## Macro (id), run as the player clicking Revert. The entry goes with the first click, so a second one cannot summon a copy.
	write_versioned_function("maps/editor/revert", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You must be in the map editor to revert.","color":"red"}}]
data remove storage {ns}:temp _ed_revert
$data modify storage {ns}:temp _ed_revert set from storage {ns}:temp map_edit.removed[{{id:$(id)}}].marker
execute unless data storage {ns}:temp _ed_revert run return run tellraw @s [{MGS_TAG},{{"text":"Already restored, or too old to revert.","color":"yellow"}}]
$data remove storage {ns}:temp map_edit.removed[{{id:$(id)}}]

execute summon minecraft:marker run function {editor}/revert_marker
function {editor}/refresh_displays
""")
	write_versioned_function("maps/editor/revert_marker", f"""
data modify entity @s {{}} merge from storage {ns}:temp _ed_revert

# Another form may target its own marker since.
tag @s remove {ns}.ed_form_target
function {editor}/sync_marker
{element_lines(ns, "restored")}
""")


def element_lines(ns: str, verb: str) -> str:
	""" Lines telling the editors, in the element's own name and colour, what happened to the marker they run as. """
	return "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo.name} {verb}!","color":"{einfo.color}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type != "config"
	)

