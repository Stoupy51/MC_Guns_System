
# ruff: noqa: E501

# Barrier System
# Physical block-display obstacles that freeze zombies entering their radius.
# Zombies can remove a barrier over 2 seconds (one remover at a time).
# Players can repair a destroyed barrier by sneaking nearby for 1.5 seconds.
# Block state is swapped in-place on destroy/repair — single block_display per barrier.

from stewbeet import Mem, write_load_file, write_versioned_function


def generate_barriers() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Scoreboards
	write_load_file(f"""
# Barrier entity scoreboards
scoreboard objectives add {ns}.zb.barrier.id dummy
scoreboard objectives add {ns}.zb.barrier.state dummy
scoreboard objectives add {ns}.zb.barrier.r_timer dummy
scoreboard objectives add {ns}.zb.barrier.rp_timer dummy
scoreboard objectives add {ns}.zb.barrier.radius dummy
scoreboard objectives add {ns}.zb.barrier.removing_id dummy
scoreboard objectives add {ns}.zb.barrier.repairing_id dummy
""")

	## Setup: iterate barrier compounds, summon block_display entities
	write_versioned_function("zombies/barriers/setup", f"""
scoreboard players set #barrier_counter {ns}.data 0
data modify storage {ns}:temp _barrier_iter set from storage {ns}:zombies game.map.barriers
execute if data storage {ns}:temp _barrier_iter[0] run function {ns}:v{version}/zombies/barriers/setup_iter
""")

	write_versioned_function("zombies/barriers/setup_iter", f"""
# Assign incrementing ID
scoreboard players add #barrier_counter {ns}.data 1

# Read position (relative) and convert to absolute
execute store result score #bx {ns}.data run data get storage {ns}:temp _barrier_iter[0].pos[0]
execute store result score #by {ns}.data run data get storage {ns}:temp _barrier_iter[0].pos[1]
execute store result score #bz {ns}.data run data get storage {ns}:temp _barrier_iter[0].pos[2]
scoreboard players operation #bx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #by {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #bz {ns}.data += #gm_base_z {ns}.data

# Read yaw from rotation[0]: float -> score*100 -> double*0.01
execute store result score #byaw {ns}.data run data get storage {ns}:temp _barrier_iter[0].rotation[0] 100

# Store positions and yaw for place_at macro
execute store result storage {ns}:temp _bplace.x double 1 run scoreboard players get #bx {ns}.data
execute store result storage {ns}:temp _bplace.y double 1 run scoreboard players get #by {ns}.data
execute store result storage {ns}:temp _bplace.z double 1 run scoreboard players get #bz {ns}.data
execute store result storage {ns}:temp _bplace.yaw double 0.01 run scoreboard players get #byaw {ns}.data

# Summon block_display
function {ns}:v{version}/zombies/barriers/place_at with storage {ns}:temp _bplace

# Copy all zb_object data onto the display (stores block_enabled, block_disabled, radius, etc.)
execute as @n[tag={ns}._barrier_new_d] run data modify entity @s data set from storage {ns}:temp _barrier_iter[0]

# Set initial block_state from block_enabled
execute as @n[tag={ns}._barrier_new_d] run data modify entity @s block_state set from entity @s data.block_enabled

# Set scoreboards on display
scoreboard players operation @n[tag={ns}._barrier_new_d] {ns}.zb.barrier.id = #barrier_counter {ns}.data
execute store result score @n[tag={ns}._barrier_new_d] {ns}.zb.barrier.radius run data get storage {ns}:temp _barrier_iter[0].radius
scoreboard players set @n[tag={ns}._barrier_new_d] {ns}.zb.barrier.state 0
scoreboard players set @n[tag={ns}._barrier_new_d] {ns}.zb.barrier.r_timer 0
scoreboard players set @n[tag={ns}._barrier_new_d] {ns}.zb.barrier.rp_timer 0

# Remove temporary tag
tag @e[tag={ns}._barrier_new_d] remove {ns}._barrier_new_d

# Continue iteration
data remove storage {ns}:temp _barrier_iter[0]
execute if data storage {ns}:temp _barrier_iter[0] run function {ns}:v{version}/zombies/barriers/setup_iter
""")

	write_versioned_function("zombies/barriers/place_at", f"""
$execute positioned $(x) $(y) $(z) align xyz positioned ~.5 ~.5 ~.5 run summon minecraft:block_display ~ ~ ~ {{Rotation:[$(yaw)f,0f],block_state:{{Name:"minecraft:air"}},transformation:{{left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],translation:[-0.5f,-0.5f,-0.5f],right_rotation:[0f,0f,0f,1f]}},brightness:{{sky:15,block:15}},Tags:["{ns}.barrier_display","{ns}.gm_entity","{ns}._barrier_new_d"]}}
""")

	## Single tick dispatch (optimization: ONE @e sweep for all barrier displays)
	write_versioned_function("zombies/barriers/tick", f"""
# @s = barrier display, at @s — dispatch by state
execute if score @s {ns}.zb.barrier.state matches 0 run function {ns}:v{version}/zombies/barriers/intact_tick
execute if score @s {ns}.zb.barrier.state matches 1 run function {ns}:v{version}/zombies/barriers/destroyed_tick

# Player collision: push players in barrier's facing direction every tick (both states)
execute rotated as @s as @a[scores={{{ns}.zb.in_game=1}},distance=..0.75] positioned as @s run tp @s ^ ^ ^0.8
""")

	## Intact barrier tick
	write_versioned_function("zombies/barriers/intact_tick", f"""
# @s = intact barrier display, at @s
execute store result score #barrier_id {ns}.data run scoreboard players get @s {ns}.zb.barrier.id
execute store result storage {ns}:temp _btick.radius int 1 run scoreboard players get @s {ns}.zb.barrier.radius

# Freeze all zombies in radius (macro)
function {ns}:v{version}/zombies/barriers/freeze_zombies with storage {ns}:temp _btick

# Handle remove timer or find a new remover (both macros using radius)
execute if score @s {ns}.zb.barrier.r_timer matches 1.. run function {ns}:v{version}/zombies/barriers/handle_removing with storage {ns}:temp _btick
execute if score @s {ns}.zb.barrier.r_timer matches 0 if score @s {ns}.zb.barrier.state matches 0 run function {ns}:v{version}/zombies/barriers/find_remover with storage {ns}:temp _btick
""")

	write_versioned_function("zombies/barriers/freeze_zombies", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(radius)] run attribute @s minecraft:movement_speed modifier add {ns}:freeze -1024 add_multiplied_total
$tag @e[tag={ns}.zombie_round,distance=..$(radius)] add {ns}.barrier_frozen
""")

	write_versioned_function("zombies/barriers/find_remover", f"""
# MACRO: @s = intact barrier marker, $(radius) = sphere radius
# Picks nearest eligible zombie and assigns it as remover
scoreboard players set #barrier_found_remover {ns}.data 0
$execute as @e[tag={ns}.zombie_round,tag=!{ns}.barrier_removing,distance=..$(radius),limit=1,sort=nearest] run function {ns}:v{version}/zombies/barriers/start_removing_zombie
execute if score #barrier_found_remover {ns}.data matches 1 run scoreboard players set @s {ns}.zb.barrier.r_timer 40
""")

	write_versioned_function("zombies/barriers/start_removing_zombie", f"""
# @s = zombie assigned as remover
tag @s add {ns}.barrier_removing
scoreboard players operation @s {ns}.zb.barrier.removing_id = #barrier_id {ns}.data
scoreboard players set #barrier_found_remover {ns}.data 1
""")

	write_versioned_function("zombies/barriers/handle_removing", f"""
# MACRO: @s = intact barrier marker, $(radius) = sphere radius
# Verify assigned remover is still in range and matches this barrier
scoreboard players set #barrier_remover_valid {ns}.data 0
$execute as @e[tag={ns}.barrier_removing,distance=..$(radius)] at @s if score @s {ns}.zb.barrier.removing_id = #barrier_id {ns}.data run function {ns}:v{version}/zombies/barriers/on_remover_valid

execute if score #barrier_remover_valid {ns}.data matches 1 run scoreboard players remove @s {ns}.zb.barrier.r_timer 1
execute if score #barrier_remover_valid {ns}.data matches 1 if score @s {ns}.zb.barrier.r_timer matches 0 run function {ns}:v{version}/zombies/barriers/destroy

# If not in range: check if remover still exists globally (alive but out of range = pause; gone = cancel)
execute if score #barrier_remover_valid {ns}.data matches 0 as @e[tag={ns}.barrier_removing] if score @s {ns}.zb.barrier.removing_id = #barrier_id {ns}.data run scoreboard players set #barrier_remover_valid {ns}.data 2
execute if score #barrier_remover_valid {ns}.data matches 0 run function {ns}:v{version}/zombies/barriers/cancel_remove
""")

	write_versioned_function("zombies/barriers/on_remover_valid", f"""
# @s = removing zombie, at zombie position (via at @s in handle_removing selector)
scoreboard players set #barrier_remover_valid {ns}.data 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 1
""")

	write_versioned_function("zombies/barriers/cancel_remove", f"""
# @s = barrier display — remover left range or died
scoreboard players set @s {ns}.zb.barrier.r_timer 0
execute as @e[tag={ns}.barrier_removing] if score @s {ns}.zb.barrier.removing_id = #barrier_id {ns}.data run tag @s remove {ns}.barrier_removing
""")

	write_versioned_function("zombies/barriers/destroy", f"""
# @s = intact barrier display → transitions to destroyed
scoreboard players set @s {ns}.zb.barrier.state 1
scoreboard players set @s {ns}.zb.barrier.r_timer 0

# Clean up removing zombie
execute as @e[tag={ns}.barrier_removing] if score @s {ns}.zb.barrier.removing_id = #barrier_id {ns}.data run tag @s remove {ns}.barrier_removing

# Switch to disabled block state
data modify entity @s block_state set from entity @s data.block_disabled

# Sound + particles
particle minecraft:large_smoke ~ ~0.5 ~ 0.4 0.4 0.4 0.02 6
particle minecraft:crit ~ ~0.5 ~ 0.4 0.4 0.4 0.05 8
playsound minecraft:entity.zombie.break_wooden_door block @a ~ ~ ~ 1.0 1.0
""")

	## Destroyed barrier tick
	write_versioned_function("zombies/barriers/destroyed_tick", f"""
# @s = destroyed barrier display, at @s
execute store result score #barrier_id {ns}.data run scoreboard players get @s {ns}.zb.barrier.id
execute store result storage {ns}:temp _brptick.radius int 1 run scoreboard players get @s {ns}.zb.barrier.radius

# Handle repair timer or find a new repairer (both macros using radius)
execute if score @s {ns}.zb.barrier.rp_timer matches 1.. run function {ns}:v{version}/zombies/barriers/handle_repair with storage {ns}:temp _brptick
execute if score @s {ns}.zb.barrier.rp_timer matches 0 if score @s {ns}.zb.barrier.state matches 1 run function {ns}:v{version}/zombies/barriers/find_repairer with storage {ns}:temp _brptick
""")

	write_versioned_function("zombies/barriers/find_repairer", f"""
# MACRO: @s = destroyed barrier marker, $(radius) = sphere radius
# Picks nearest sneaking in-game player and assigns them as repairer
scoreboard players set #barrier_found_repairer {ns}.data 0
$execute as @a[scores={{{ns}.zb.in_game=1}},predicate={ns}:v{version}/is_sneaking,distance=..$(radius),tag=!{ns}.barrier_repairing,limit=1,sort=nearest] run function {ns}:v{version}/zombies/barriers/start_repairing_player
execute if score #barrier_found_repairer {ns}.data matches 1 run scoreboard players set @s {ns}.zb.barrier.rp_timer 30
""")

	write_versioned_function("zombies/barriers/start_repairing_player", f"""
# @s = player assigned as repairer
tag @s add {ns}.barrier_repairing
scoreboard players operation @s {ns}.zb.barrier.repairing_id = #barrier_id {ns}.data
scoreboard players set #barrier_found_repairer {ns}.data 1
""")

	write_versioned_function("zombies/barriers/handle_repair", f"""
# MACRO: @s = destroyed barrier marker, $(radius) = sphere radius
# Verify assigned repairer is still valid (sneaking, in range, correct id)
execute store result score #barrier_rp_cur {ns}.data run scoreboard players get @s {ns}.zb.barrier.rp_timer
scoreboard players set #barrier_repair_valid {ns}.data 0
$execute as @a[tag={ns}.barrier_repairing,distance=..$(radius)] if score @s {ns}.zb.barrier.repairing_id = #barrier_id {ns}.data if predicate {ns}:v{version}/is_sneaking run function {ns}:v{version}/zombies/barriers/on_repairer_valid

execute if score #barrier_repair_valid {ns}.data matches 0 run function {ns}:v{version}/zombies/barriers/cancel_repair
execute if score #barrier_repair_valid {ns}.data matches 1 run scoreboard players remove @s {ns}.zb.barrier.rp_timer 1
execute if score #barrier_repair_valid {ns}.data matches 1 if score @s {ns}.zb.barrier.rp_timer matches 0 run function {ns}:v{version}/zombies/barriers/repair
""")

	write_versioned_function("zombies/barriers/on_repairer_valid", f"""
# @s = repairing player
scoreboard players set #barrier_repair_valid {ns}.data 1
# Actionbar progress: show remaining ticks out of 30
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🔧 Repairing barrier... ","color":"aqua"}},{{"score":{{"name":"#barrier_rp_cur","objective":"{ns}.data"}},"color":"yellow"}},{{"text":"/30","color":"gray"}}],priority:"notification",freeze:2}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/barriers/cancel_repair", f"""
# @s = barrier display — repairer stopped sneaking or left range
scoreboard players set @s {ns}.zb.barrier.rp_timer 0
execute as @a[tag={ns}.barrier_repairing] if score @s {ns}.zb.barrier.repairing_id = #barrier_id {ns}.data run tag @s remove {ns}.barrier_repairing
""")

	write_versioned_function("zombies/barriers/repair", f"""
# @s = destroyed barrier display → transitions back to intact
scoreboard players set @s {ns}.zb.barrier.state 0
scoreboard players set @s {ns}.zb.barrier.rp_timer 0

# Clean up repairing player tag and show success
execute as @a[tag={ns}.barrier_repairing] if score @s {ns}.zb.barrier.repairing_id = #barrier_id {ns}.data run function {ns}:v{version}/zombies/barriers/on_repair_complete_player

# Switch back to enabled block state
data modify entity @s block_state set from entity @s data.block_enabled

# Clear any leftover barrier_removing tag from zombies associated with this barrier
execute as @e[tag={ns}.barrier_removing] if score @s {ns}.zb.barrier.removing_id = #barrier_id {ns}.data run tag @s remove {ns}.barrier_removing

# Sound + particles
particle minecraft:happy_villager ~ ~1 ~ 0.5 0.5 0.5 0 10
playsound minecraft:block.anvil.use block @a ~ ~ ~ 1.0 1.5
""")

	write_versioned_function("zombies/barriers/on_repair_complete_player", f"""
# @s = repairing player
tag @s remove {ns}.barrier_repairing
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"✔ Barrier repaired!","color":"green"}}],priority:"notification",freeze:20}}
function #smithed.actionbar:message
""")

	## Restore zombie movement speed after barrier freeze (called before freeze each tick)
	write_versioned_function("zombies/barriers/restore_zombie_speed", f"""
# @s = frozen zombie — restore level-appropriate speed
attribute @s minecraft:movement_speed modifier remove {ns}:freeze
tag @s remove {ns}.barrier_frozen
""")

	## Hook into game tick — single @e sweep for all barrier displays
	write_versioned_function("zombies/game_tick", f"""
# Barriers: restore frozen speeds from last tick, then dispatch all display ticks
execute as @e[tag={ns}.zombie_round,tag={ns}.barrier_frozen] run function {ns}:v{version}/zombies/barriers/restore_zombie_speed
execute as @e[tag={ns}.barrier_display] at @s run function {ns}:v{version}/zombies/barriers/tick
""")

	## Hook into preload_complete — setup barriers if map has any
	write_versioned_function("zombies/preload_complete", f"""
# Setup barriers
execute if data storage {ns}:zombies game.map.barriers[0] run function {ns}:v{version}/zombies/barriers/setup
""")

	## Hook into stop — clean up tags on living entities (gm_entity kill handles the entities)
	write_versioned_function("zombies/stop", f"""
# Barriers cleanup
tag @e[tag={ns}.barrier_removing] remove {ns}.barrier_removing
tag @a[tag={ns}.barrier_repairing] remove {ns}.barrier_repairing
""")

