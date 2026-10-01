""" Spawning a box per map position, hiding the dead ones and moving the active one. """
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import MB_CLOSED_TF, MB_OPEN_TF


# Functions
def write_mystery_box_positions() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/mystery_box/setup_positions", f"""
scoreboard players set #mb_box_counter {ns}.data 0

# In box-id order, so names[id - 1] is a box's name ("" when unnamed).
data modify storage {ns}:zombies mystery_box.names set value []

data modify storage {ns}:temp _mb_iter set from storage {ns}:zombies game.map.mystery_box.positions
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter

# The active box starts at a random can_start_on position, else any position.
execute as @n[tag={ns}.mystery_box_pos,tag={ns}.mb_can_start,sort=random] run tag @s add {ns}.mystery_box_active
execute unless entity @e[tag={ns}.mystery_box_active] as @n[tag={ns}.mystery_box_pos,sort=random] run tag @s add {ns}.mystery_box_active

scoreboard players set #mb_pulls {ns}.data 0
scoreboard players set #mb_box_counter {ns}.data 0
function {ns}:v{version}/zombies/mystery_box/sync_presence_display

function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

	write_versioned_function("zombies/mystery_box/setup_pos_iter", f"""
execute store result score #mbx {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[0]
execute store result score #mby {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[1]
execute store result score #mbz {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[2]

scoreboard players operation #mbx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #mby {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #mbz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _mbpos.x double 1 run scoreboard players get #mbx {ns}.data
execute store result storage {ns}:temp _mbpos.y double 1 run scoreboard players get #mby {ns}.data
execute store result storage {ns}:temp _mbpos.z double 1 run scoreboard players get #mbz {ns}.data
data modify storage {ns}:temp _mbpos.rotation set from storage {ns}:temp _mb_iter[0].rotation

function {ns}:v{version}/zombies/mystery_box/summon_pos_at with storage {ns}:temp _mbpos
execute as @n[tag={ns}.mb_new] at @s run tp @s ^ ^2 ^0.3

# Shared later by its pull display.
scoreboard players add #mb_box_counter {ns}.data 1
scoreboard players operation @n[tag={ns}.mb_new] {ns}.mb.box = #mb_box_counter {ns}.data

data modify storage {ns}:temp _mb_name set value ""
execute if data storage {ns}:temp _mb_iter[0].location_name run data modify storage {ns}:temp _mb_name set from storage {ns}:temp _mb_iter[0].location_name
data modify storage {ns}:zombies mystery_box.names append from storage {ns}:temp _mb_name

data modify storage {ns}:temp can_start_on set from storage {ns}:temp _mb_iter[0].can_start_on
execute if data storage {ns}:temp {{can_start_on:1b}} run tag @n[tag={ns}.mb_new] add {ns}.mb_can_start

execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/mystery_box/on_right_click",executor:"source"}}
execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/mystery_box/on_hover",executor:"source"}}
execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_left_click {{run:"function {ns}:v{version}/zombies/mystery_box/on_left_click",executor:"source"}}
tag @n[tag={ns}.mb_new] remove {ns}.mb_new

data remove storage {ns}:temp _mb_iter[0]
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter
""")

	write_versioned_function("zombies/mystery_box/summon_pos_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:2.0f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.mystery_box_pos","{ns}.gm_entity","{ns}.mb_new","bs.entity.interaction"]}}
""")

	## Unusable boxes (not active, no Fire Sale, no pull in progress) have their interaction moved 512 blocks away, so it cannot be hovered or eat a gun click.
	## Run on every state change (setup, move, Fire Sale, collect), never per tick.
	write_versioned_function("zombies/mystery_box/sync_interaction_visibility", f"""
execute as @e[tag={ns}.mystery_box_pos] at @s run function {ns}:v{version}/zombies/mystery_box/sync_interaction_one
""")

	write_versioned_function("zombies/mystery_box/sync_interaction_one", f"""
# Run as a box interaction entity, at it.
scoreboard players set #mb_vis {ns}.data 0
execute if entity @s[tag={ns}.mystery_box_active] run scoreboard players set #mb_vis {ns}.data 1
execute if score #zb_fire_sale_timer {ns}.data matches 1.. if entity @s[tag={ns}.mb_fs_active] run scoreboard players set #mb_vis {ns}.data 1
execute if entity @n[tag={ns}.mb_display,distance=..3] run scoreboard players set #mb_vis {ns}.data 1

execute if score #mb_vis {ns}.data matches 1 if entity @s[tag={ns}.roam_hidden] run function {ns}:v{version}/zombies/roaming/interaction_show
execute if score #mb_vis {ns}.data matches 0 unless entity @s[tag={ns}.roam_hidden] run function {ns}:v{version}/zombies/roaming/interaction_hide
""")

	## An open chest at the active box and a grayed crate at every inactive spot, showing where the box can roam.
	## During a Fire Sale the inactive spots hold real temporary boxes, so there are no grayed crates.
	write_versioned_function("zombies/mystery_box/sync_presence_display", f"""
kill @e[tag={ns}.mb_presence]
kill @e[tag={ns}.mb_disabled]
execute as @n[tag={ns}.mystery_box_active] at @s run data modify storage {ns}:temp _mb_chest.yaw set value 0.0f
execute as @n[tag={ns}.mystery_box_active] at @s run data modify storage {ns}:temp _mb_chest.yaw set from entity @s Rotation[0]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/mystery_box/summon_presence_display with storage {ns}:temp _mb_chest

function {ns}:v{version}/zombies/mystery_box/refresh_disabled
""")

	## Only the grayed crates, so it can run after a move lands without touching the new chest. None during a Fire Sale.
	write_versioned_function("zombies/mystery_box/refresh_disabled", f"""
kill @e[tag={ns}.mb_disabled]
execute if score #zb_fire_sale_timer {ns}.data matches ..0 as @e[tag={ns}.mystery_box_pos,tag=!{ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/mystery_box/summon_disabled_display
""")

	## Run as an inactive box interaction entity, at it: same model as the chest, 0.9 below, no lid.
	## Skips a box with a pull in progress (its result shows there), and shifts back up 512 for a hidden entity (see interaction_hide).
	write_versioned_function("zombies/mystery_box/summon_disabled_display", f"""
execute if entity @n[tag={ns}.mb_display,distance=..3] run return 0
data modify storage {ns}:temp _mb_dis.yaw set value 0.0f
data modify storage {ns}:temp _mb_dis.yaw set from entity @s Rotation[0]
execute unless entity @s[tag={ns}.roam_hidden] run function {ns}:v{version}/zombies/mystery_box/summon_disabled_at with storage {ns}:temp _mb_dis
execute if entity @s[tag={ns}.roam_hidden] positioned ~ ~512 ~ run function {ns}:v{version}/zombies/mystery_box/summon_disabled_at with storage {ns}:temp _mb_dis
""")

	write_versioned_function("zombies/mystery_box/summon_disabled_at", f"""
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_disabled","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_disabled"}}}},transformation:{MB_CLOSED_TF}}}
""")

	write_versioned_function("zombies/mystery_box/summon_presence_display", f"""
# Base and lid share mb_presence, so they move and despawn together.
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_base","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{MB_CLOSED_TF}}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_lid","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{MB_CLOSED_TF}}}
""")

	## Affects the lid nearest the execution position: callers must stand at their box.
	write_versioned_function("zombies/mystery_box/open_lid", f"""
data merge entity @n[tag={ns}.mb_lid,distance=..4] {{transformation:{MB_OPEN_TF},start_interpolation:0,interpolation_duration:8}}
""")
	write_versioned_function("zombies/mystery_box/close_lid", f"""
data merge entity @n[tag={ns}.mb_lid,distance=..4] {{transformation:{MB_CLOSED_TF},start_interpolation:0,interpolation_duration:8}}
""")

	write_versioned_function("zombies/mystery_box/move_active_position", f"""
execute store result score #mb_pos_count {ns}.data run data get storage {ns}:zombies game.map.mystery_box.positions
execute if score #mb_pos_count {ns}.data matches ..1 run return 0

tag @e[tag={ns}.mystery_box_active] add {ns}.mb_prev_active
tag @e[tag={ns}.mystery_box_active] remove {ns}.mystery_box_active
execute as @n[tag={ns}.mystery_box_pos,tag=!{ns}.mb_prev_active,sort=random] run tag @s add {ns}.mystery_box_active
tag @e[tag={ns}.mb_prev_active] remove {ns}.mb_prev_active
""")

