
# ruff: noqa: E501
# Mystery Box System
# Dynamic weapon pool, visual animation with item cycling, random selection.
# Price: 950 points (configurable via #zb_mystery_box_price config)
# Pool can be extended via function tag #mgs:zombies/register_mystery_box_item
# Uses Bookshelf interaction module for click/hover detection.
# Positions use compound format: {pos:[x,y,z], rotation:[yaw,0.0f], group_id:N, can_start_on:1b}

from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


def generate_mystery_box() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Setup: iterate mystery box position compounds, summon interaction entities with Bookshelf
	write_versioned_function("zombies/mystery_box/setup_positions", f"""
# Summon mystery box markers at map positions
data modify storage {ns}:temp _mb_iter set from storage {ns}:zombies game.map.mystery_box.positions
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter

# Pick a random position with can_start_on as the active mystery box
execute as @n[tag={ns}.mystery_box_pos,tag={ns}.mb_can_start,sort=random] run tag @s add {ns}.mystery_box_active
# Fallback if no can_start_on positions exist
execute unless entity @e[tag={ns}.mystery_box_active] as @n[tag={ns}.mystery_box_pos,sort=random] run tag @s add {ns}.mystery_box_active
""")

	write_versioned_function("zombies/mystery_box/setup_pos_iter", f"""
# Read relative position from compound and convert to absolute
execute store result score #_mbx {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[0]
execute store result score #_mby {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[1]
execute store result score #_mbz {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[2]

scoreboard players operation #_mbx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #_mby {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #_mbz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _mbpos.x double 1 run scoreboard players get #_mbx {ns}.data
execute store result storage {ns}:temp _mbpos.y double 1 run scoreboard players get #_mby {ns}.data
execute store result storage {ns}:temp _mbpos.z double 1 run scoreboard players get #_mbz {ns}.data

function {ns}:v{version}/zombies/mystery_box/summon_pos_at with storage {ns}:temp _mbpos

# Tag entities that can_start_on
data modify storage {ns}:temp can_start_on set from storage {ns}:temp _mb_iter[0].can_start_on
execute if data storage {ns}:temp {{can_start_on:1b}} run tag @n[tag={ns}._mb_new] add {ns}.mb_can_start

# Register Bookshelf events on newly spawned entity
execute as @n[tag={ns}._mb_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/mystery_box/on_right_click",executor:"source"}}
execute as @n[tag={ns}._mb_new] run function #bs.interaction:on_hover_enter {{run:"function {ns}:v{version}/zombies/mystery_box/on_hover_enter",executor:"source"}}
execute as @n[tag={ns}._mb_new] run function #bs.interaction:on_hover_leave {{run:"function {ns}:v{version}/zombies/mystery_box/on_hover_leave",executor:"source"}}
tag @n[tag={ns}._mb_new] remove {ns}._mb_new

data remove storage {ns}:temp _mb_iter[0]
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter
""")

	write_versioned_function("zombies/mystery_box/summon_pos_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.0f,height:1.0f,response:true,Tags:["{ns}.mystery_box_pos","{ns}.gm_entity","{ns}._mb_new","bs.entity.interaction"]}}
""")

	## On right-click: Bookshelf callback (executor:"source" = @s is the player)
	write_versioned_function("zombies/mystery_box/on_right_click", f"""
# Only respond if this is the active mystery box
execute unless entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return fail

# Check game is active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# If result is ready: collect
execute if data storage {ns}:zombies mystery_box{{ready:true}} run return run function {ns}:v{version}/zombies/mystery_box/collect

# If already spinning: inform player
execute if data storage {ns}:zombies mystery_box{{spinning:true}} run return run tellraw @s [{MGS_TAG},{{"text":"Mystery Box is already in use!","color":"red"}}]

# Otherwise: try to use (buy)
function {ns}:v{version}/zombies/mystery_box/try_use
""")

	write_versioned_function("zombies/mystery_box/try_use", f"""
# Check if player has enough points
execute unless score @s {ns}.zb.points >= #zb_mystery_box_price {ns}.config run return run tellraw @s [{MGS_TAG},{{"text":"Not enough points! (950 required)","color":"red"}}]

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #zb_mystery_box_price {ns}.config

# Start spinning
data modify storage {ns}:zombies mystery_box.spinning set value true

# Pick a random weapon from the pool
execute store result score #_mb_pool_size {ns}.data run data get storage {ns}:zombies mystery_box_pool
execute if score #_mb_pool_size {ns}.data matches ..0 run return run tellraw @s [{MGS_TAG},{{"text":"Mystery Box pool is empty!","color":"red"}}]
execute store result score #_mb_pick {ns}.data run random value 0..100
scoreboard players operation #_mb_pick {ns}.data %= #_mb_pool_size {ns}.data

# Copy pool and iterate to the picked index
data modify storage {ns}:temp _mb_pool_iter set from storage {ns}:zombies mystery_box_pool
function {ns}:v{version}/zombies/mystery_box/pick_item

# Store the result
data modify storage {ns}:zombies mystery_box.result set from storage {ns}:temp _mb_pool_iter[0]

# Start animation timer (40 ticks cycling + 60 ticks display = 100 total)
scoreboard players set #mb_anim_timer {ns}.data 40

# Spawn display entity at box position
execute at @n[tag={ns}.mystery_box_active] run function {ns}:v{version}/zombies/mystery_box/spawn_display

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Mystery Box spinning...","color":"light_purple"}}]
""")

	write_versioned_function("zombies/mystery_box/pick_item", f"""
execute if score #_mb_pick {ns}.data matches 1.. run data remove storage {ns}:temp _mb_pool_iter[0]
execute if score #_mb_pick {ns}.data matches 1.. run scoreboard players remove #_mb_pick {ns}.data 1
execute if score #_mb_pick {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/pick_item
""")

	## Display entity: spawns at box level, floats up with interpolation
	write_versioned_function("zombies/mystery_box/spawn_display", f"""
# Spawn item display at box level with initial small scale
summon minecraft:item_display ~ ~0.5 ~ {{Tags:["{ns}.mb_display","{ns}.gm_entity"],item:{{id:"minecraft:nether_star",count:1}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.5f,0.5f,0.5f]}},billboard:"center",interpolation_duration:10}}

# Float up: set target transformation and trigger interpolation
data merge entity @n[tag={ns}.mb_display] {{transformation:{{translation:[0f,0.8f,0f],scale:[0.7f,0.7f,0.7f]}},start_interpolation:0}}
""")

	## Mystery box tick: handle animation
	write_versioned_function("zombies/mystery_box/tick", f"""
# Only tick if spinning
execute unless data storage {ns}:zombies mystery_box{{spinning:true}} run return 0

# Decrement timer
scoreboard players remove #mb_anim_timer {ns}.data 1

# Cycling phase (timer > 0): show random items
execute if score #mb_anim_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/cycle_display

# Landing phase (timer = 0): show the result
execute if score #mb_anim_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/show_result

# Pickup window expired (timer = -60): remove display and reset
execute if score #mb_anim_timer {ns}.data matches ..-60 run function {ns}:v{version}/zombies/mystery_box/reset
""")

	## Cycle display: swap the item_display model to simulate cycling
	write_versioned_function("zombies/mystery_box/cycle_display", f"""
# Pick a random item from pool to display
execute store result score #_mb_cycle {ns}.data run random value 0..100
execute store result score #_mb_ps {ns}.data run data get storage {ns}:zombies mystery_box_pool
scoreboard players operation #_mb_cycle {ns}.data %= #_mb_ps {ns}.data

data modify storage {ns}:temp _mb_cycle_iter set from storage {ns}:zombies mystery_box_pool
function {ns}:v{version}/zombies/mystery_box/cycle_iterate

# Apply the cycled item directly to the display entity
data modify entity @n[tag={ns}.mb_display] item set from storage {ns}:temp _mb_cycle_iter[0].display_item
""")

	write_versioned_function("zombies/mystery_box/cycle_iterate", f"""
execute if score #_mb_cycle {ns}.data matches 1.. run data remove storage {ns}:temp _mb_cycle_iter[0]
execute if score #_mb_cycle {ns}.data matches 1.. run scoreboard players remove #_mb_cycle {ns}.data 1
execute if score #_mb_cycle {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/cycle_iterate
""")

	## Show result: display the final picked weapon with interpolation
	write_versioned_function("zombies/mystery_box/show_result", f"""
# Set display to final result
data modify entity @n[tag={ns}.mb_display] item set from storage {ns}:zombies mystery_box.result.display_item

# Smooth settle to final position with interpolation
data merge entity @n[tag={ns}.mb_display] {{transformation:{{translation:[0f,1.0f,0f],scale:[0.8f,0.8f,0.8f]}},start_interpolation:0}}

# Tag the box as ready for pickup
data modify storage {ns}:zombies mystery_box.ready set value true

# Announce result
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Mystery Box result ready! ","color":"light_purple"}},{{"text":"Right-click to collect!","color":"green","bold":true}}]
""")

	## Collect the mystery box result (called from on_right_click, @s = player)
	write_versioned_function("zombies/mystery_box/collect", f"""
# Give the result item to the player via its give function
execute if data storage {ns}:zombies mystery_box.result.give_function run function {ns}:v{version}/zombies/mystery_box/give_via_function

# Announce
tellraw @s [{MGS_TAG},{{"text":"You collected a weapon from the Mystery Box!","color":"green"}}]

# Reset box
function {ns}:v{version}/zombies/mystery_box/reset
""")

	write_versioned_function("zombies/mystery_box/give_via_function", f"""
function {ns}:v{version}/zombies/mystery_box/run_give with storage {ns}:zombies mystery_box.result
""")

	write_versioned_function("zombies/mystery_box/run_give", """
$function $(give_function)
""")

	## Reset mystery box state
	write_versioned_function("zombies/mystery_box/reset", f"""
# Kill display entity
kill @e[tag={ns}.mb_display]

# Reset state
data modify storage {ns}:zombies mystery_box.spinning set value false
data modify storage {ns}:zombies mystery_box.ready set value false
data remove storage {ns}:zombies mystery_box.result
""")

	## Hover functions for active mystery box
	write_versioned_function("zombies/mystery_box/on_hover_enter", f"""
execute unless entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return fail
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute if data storage {ns}:zombies mystery_box{{ready:true}} run return run title @s actionbar [{{"text":"Mystery Box","color":"light_purple","bold":true}},{{"text":" - ","color":"gray"}},{{"text":"Click to collect!","color":"green"}}]
execute if data storage {ns}:zombies mystery_box{{spinning:true}} run return run title @s actionbar [{{"text":"Mystery Box","color":"light_purple","bold":true}},{{"text":" - ","color":"gray"}},{{"text":"Spinning...","color":"yellow"}}]
title @s actionbar [{{"text":"Mystery Box","color":"light_purple","bold":true}},{{"text":" - ","color":"gray"}},{{"text":"950 points","color":"gold"}}]
""")

	write_versioned_function("zombies/mystery_box/on_hover_leave", """
title @s actionbar ""
""")

	## Hook into game tick for mystery box animation only (interaction handled by Bookshelf)
	write_versioned_function("zombies/game_tick", f"""
# Mystery box animation tick
function {ns}:v{version}/zombies/mystery_box/tick
""")

	## Hook into game start to setup mystery box positions
	write_versioned_function("zombies/preload_complete", f"""
# Setup mystery box positions
execute if data storage {ns}:zombies game.map.mystery_box.positions[0] run function {ns}:v{version}/zombies/mystery_box/setup_positions
""")

	## Hook into stop to reset mystery box
	write_versioned_function("zombies/stop", f"""
# Reset mystery box
function {ns}:v{version}/zombies/mystery_box/reset
""")
