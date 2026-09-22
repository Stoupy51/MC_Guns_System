""" The real in-game models shown next to the markers while editing. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS, MODEL_DISPLAY_ELEMENTS
from .shared import snbt_suggest


# Functions
def write_editor_displays() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Model Displays.
	# Show the real in-game models for wallbuys, perk machines, PAP, mystery boxes, and the power switch while editing.
	# Displays are rebuilt on placement/destroy, and by displays/sync once a second when a marker was edited, so rotation or item_model changes stay in sync.
	# Each displays/<etype> function mirrors that system's own setup placement exactly.
	model_markers: str = f"@e[type=minecraft:marker,tag={ns}.model_display]"
	write_versioned_function("maps/editor/refresh_displays", f"""
# Rebuild all editor model displays from the current markers
kill @e[tag={ns}.editor_display]
{"\n".join(
	f"execute as @e[type=minecraft:marker,tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/displays/{etype}"
	for etype in MODEL_DISPLAY_ELEMENTS
)}

# Snapshot what was just drawn, so displays/sync only rebuilds after a real edit
{"\n".join(f"tag @e[type=minecraft:marker,tag={ns}.element.{etype}] add {ns}.model_display" for etype in MODEL_DISPLAY_ELEMENTS)}
execute as {model_markers} run function {ns}:v{version}/maps/editor/displays/snapshot
execute store result score #ed_disp_count {ns}.data if entity {model_markers}
""")

	# Killing and summoning the displays makes them blink for a frame, so a rebuild only happens when a marker changed.
	write_versioned_function("maps/editor/displays/sync", f"""
scoreboard players set #ed_disp_dirty {ns}.data 0
execute as {model_markers} run function {ns}:v{version}/maps/editor/displays/snapshot
execute store result score #ed_disp_now {ns}.data if entity {model_markers}
execute unless score #ed_disp_now {ns}.data = #ed_disp_count {ns}.data run scoreboard players set #ed_disp_dirty {ns}.data 1
execute if score #ed_disp_dirty {ns}.data matches 1 run function {ns}:v{version}/maps/editor/refresh_displays
""")
	write_versioned_function("maps/editor/displays/snapshot", f"""
# @s = a model-display marker. Everything its display is built from is its data and position.
data modify storage {ns}:temp _ed_sig set value {{}}
data modify storage {ns}:temp _ed_sig.data set from entity @s data
data remove storage {ns}:temp _ed_sig.data._disp_sig
data modify storage {ns}:temp _ed_sig.pos set from entity @s Pos
execute store success score #ed_sig_changed {ns}.data run data modify entity @s data._disp_sig set from storage {ns}:temp _ed_sig
execute if score #ed_sig_changed {ns}.data matches 1 run scoreboard players set #ed_disp_dirty {ns}.data 1
""")

	## Barricade: block_display of the "enabled" (intact) block, mirroring zombies/barricades/place_at so a map maker sees the boards exactly where they will stand in game.
	write_versioned_function("maps/editor/displays/barricade", f"""
# @s = barricade marker, at @s
data modify storage {ns}:temp _ed_bar.yaw set value 0.0f
execute if data entity @s data.yaw run data modify storage {ns}:temp _ed_bar.yaw set from entity @s data.yaw

# Fall back to the element default when the marker has no block configured yet
data modify storage {ns}:temp _ed_bar.block set value {snbt_suggest(ALL_ELEMENTS["barricade"].defaults["block_enabled"])}
execute if data entity @s data.block_enabled run data modify storage {ns}:temp _ed_bar.block set from entity @s data.block_enabled

execute align xyz positioned ~.5 ~.5 ~.5 run function {ns}:v{version}/maps/editor/displays/summon_barricade with storage {ns}:temp _ed_bar
""")
	write_versioned_function("maps/editor/displays/summon_barricade", f"""
# Same placement and transform as zombies/barricades/place_at
$summon minecraft:block_display ~ ~ ~ {{Rotation:[$(yaw),0f],block_state:$(block),transformation:{{left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],translation:[-0.5f,-0.5f,-0.5f],right_rotation:[0f,0f,0f,1f]}},Tags:["{ns}.editor_display"]}}
""")

	## Wallbuy: weapon item display against the wall (same placement/scale as zombies/wallbuys setup)
	write_versioned_function("maps/editor/displays/wallbuy", f"""
# @s = wallbuy marker, at @s (marker Rotation is synced from data.yaw)
data modify storage {ns}:temp _ed_disp.weapon_id set from entity @s data.weapon_id
data modify storage {ns}:temp _ed_disp.yaw set value 0.0f
data modify storage {ns}:temp _ed_disp.yaw set from entity @s data.yaw
function {ns}:v{version}/maps/editor/displays/summon_wallbuy with storage {ns}:temp _ed_disp
""")
	write_versioned_function("maps/editor/displays/summon_wallbuy", f"""
# Display offset up + toward the wall face, scale 0.6 (mirrors zombies/wallbuys/place_at + tp)
$summon minecraft:item_display ^ ^0.5 ^-0.49 {{Rotation:[$(yaw),0f],billboard:"fixed",item_display:"fixed",Tags:["{ns}.editor_display","{ns}._ed_new_disp"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}
$execute as @n[tag={ns}._ed_new_disp] run loot replace entity @s contents loot {ns}:i/$(weapon_id)
tag @e[tag={ns}._ed_new_disp] remove {ns}._ed_new_disp
""")

	## Perk machine: mirror zombies/perks/setup_iter display logic (default potion model with per-perk override; map-defined display_item/item_model take precedence)
	write_versioned_function("maps/editor/displays/perk_machine", f"""
# @s = perk machine marker, at @s
data modify storage {ns}:temp _pk_disp.tag set value "{ns}.editor_display"
data modify storage {ns}:temp _pk_disp.item_id set value ""
data modify storage {ns}:temp _pk_disp.item_model set value ""
data modify storage {ns}:temp _pk_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage {ns}:temp _pk_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage {ns}:temp _pk_disp.item_model set from entity @s data.item_model
execute if data storage {ns}:temp _pk_disp{{item_id:""}} run data modify storage {ns}:temp _pk_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _pk_disp{{item_model:""}} run data modify storage {ns}:temp _pk_disp.item_model set value "minecraft:potion"
data modify storage {ns}:temp _pk_disp.perk_id set from entity @s data.perk_id
execute if data storage {ns}:temp _pk_disp{{item_model:"minecraft:potion"}} run function {ns}:v{version}/zombies/perks/override_perk_model with storage {ns}:temp _pk_disp
execute if data entity @s data.yaw run data modify storage {ns}:temp _pk_disp.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pk_disp
""")

	## Der Wunderfizz: mirror zombies/wunderfizz/setup_iter display logic (perk-machine pipeline)
	write_versioned_function("maps/editor/displays/wunderfizz", f"""
# @s = wunderfizz marker, at @s
data modify storage {ns}:temp _wf_disp.tag set value "{ns}.editor_display"
data modify storage {ns}:temp _wf_disp.item_id set value ""
data modify storage {ns}:temp _wf_disp.item_model set value ""
data modify storage {ns}:temp _wf_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage {ns}:temp _wf_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage {ns}:temp _wf_disp.item_model set from entity @s data.item_model
execute if data storage {ns}:temp _wf_disp{{item_id:""}} run data modify storage {ns}:temp _wf_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _wf_disp{{item_model:""}} run data modify storage {ns}:temp _wf_disp.item_model set value "{ns}:der_wunderfizz"
execute if data entity @s data.yaw run data modify storage {ns}:temp _wf_disp.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _wf_disp
""")

	## Pack-a-Punch: mirror zombies/pap/setup_iter display logic
	write_versioned_function("maps/editor/displays/pap_machine", f"""
# @s = pap machine marker, at @s
data modify storage {ns}:temp _pap_disp.tag set value "{ns}.editor_display"
data modify storage {ns}:temp _pap_disp.item_id set value ""
data modify storage {ns}:temp _pap_disp.item_model set value ""
data modify storage {ns}:temp _pap_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage {ns}:temp _pap_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage {ns}:temp _pap_disp.item_model set from entity @s data.item_model
execute if data storage {ns}:temp _pap_disp{{item_id:""}} run data modify storage {ns}:temp _pap_disp.item_id set value "minecraft:netherite_block"
execute if data storage {ns}:temp _pap_disp{{item_model:""}} run data modify storage {ns}:temp _pap_disp.item_model set value "{ns}:pack_a_punch"
execute if data entity @s data.yaw run data modify storage {ns}:temp _pap_disp.yaw set from entity @s data.yaw
execute positioned ^ ^ ^-0.49 positioned ~ ~-0.4 ~ run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pap_disp
""")

	## Mystery box: two-piece chest (base + lid).
	## The in-game box interaction sits at ^ ^2 ^0.3 from the map position and the presence chest is drawn 0.9 below it (see zombies/mystery_box).
	write_versioned_function("maps/editor/displays/mystery_box_pos", f"""
# @s = mystery box marker, at @s
data modify storage {ns}:temp _ed_mb.yaw set value 0.0f
data modify storage {ns}:temp _ed_mb.yaw set from entity @s data.yaw
execute positioned ^ ^2 ^0.3 run function {ns}:v{version}/maps/editor/displays/summon_mystery_box with storage {ns}:temp _ed_mb
""")
	write_versioned_function("maps/editor/displays/summon_mystery_box", f"""
# Same models/scale as zombies/mystery_box/summon_presence_display
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.editor_display"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.editor_display"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}}}
""")

	## Power switch: block-centered lever display (same as zombies/power setup)
	write_versioned_function("maps/editor/displays/power_switch", f"""
# @s = power switch marker, at @s
data modify storage {ns}:temp _ed_ps.yaw set value 0.0f
data modify storage {ns}:temp _ed_ps.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~.5 ~.5 run function {ns}:v{version}/maps/editor/displays/summon_power_switch with storage {ns}:temp _ed_ps
""")
	write_versioned_function("maps/editor/displays/summon_power_switch", f"""
$summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.editor_display"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:lever",count:1,components:{{"minecraft:item_model":"{ns}:power_switch"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}}}
""")

