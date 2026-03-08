
# ruff: noqa: E501
# Trap System
# Area-of-effect devices that damage zombies in a radius for a duration, then enter cooldown.
# Type 0 = fire damage, Type 1 = electric (instant kill).
from stewbeet import Mem, write_load_file, write_versioned_function

from ..helpers import MGS_TAG


def generate_traps() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Trap entity scoreboards
	write_load_file(f"""
# Trap entity scoreboards
scoreboard objectives add {ns}.zb.trap.id dummy
scoreboard objectives add {ns}.zb.trap.price dummy
scoreboard objectives add {ns}.zb.trap.power dummy
scoreboard objectives add {ns}.zb.trap.type dummy
scoreboard objectives add {ns}.zb.trap.dur dummy
scoreboard objectives add {ns}.zb.trap.cd_max dummy
scoreboard objectives add {ns}.zb.trap.timer dummy
scoreboard objectives add {ns}.zb.trap.cd dummy
scoreboard objectives add {ns}.zb.trap.radius dummy
""")

	## Setup: iterate trap compounds, summon interaction + marker entities
	write_versioned_function("zombies/traps/setup", f"""
scoreboard players set #trap_counter {ns}.data 0
data modify storage {ns}:temp _trap_iter set from storage {ns}:zombies game.map.traps
execute if data storage {ns}:temp _trap_iter[0] run function {ns}:v{version}/zombies/traps/setup_iter
""")

	write_versioned_function("zombies/traps/setup_iter", f"""
# Assign incrementing ID
scoreboard players add #trap_counter {ns}.data 1

# Read trap center position (relative) and convert to absolute
execute store result score #tx {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[0]
execute store result score #ty {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[1]
execute store result score #tz {ns}.data run data get storage {ns}:temp _trap_iter[0].pos[2]
scoreboard players operation #tx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #ty {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #tz {ns}.data += #gm_base_z {ns}.data

# Compute interaction entity position (trap center + offset_pos)
execute store result score #tix {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[0]
execute store result score #tiy {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[1]
execute store result score #tiz {ns}.data run data get storage {ns}:temp _trap_iter[0].offset_pos[2]
scoreboard players operation #tix {ns}.data += #tx {ns}.data
scoreboard players operation #tiy {ns}.data += #ty {ns}.data
scoreboard players operation #tiz {ns}.data += #tz {ns}.data

# Store positions for macros
execute store result storage {ns}:temp _trap.cx int 1 run scoreboard players get #tx {ns}.data
execute store result storage {ns}:temp _trap.cy int 1 run scoreboard players get #ty {ns}.data
execute store result storage {ns}:temp _trap.cz int 1 run scoreboard players get #tz {ns}.data
execute store result storage {ns}:temp _trap.ix int 1 run scoreboard players get #tix {ns}.data
execute store result storage {ns}:temp _trap.iy int 1 run scoreboard players get #tiy {ns}.data
execute store result storage {ns}:temp _trap.iz int 1 run scoreboard players get #tiz {ns}.data

# Summon entities
function {ns}:v{version}/zombies/traps/place_at with storage {ns}:temp _trap

# Set scoreboards on interaction entity
scoreboard players operation @n[tag=_trap_new_i] {ns}.zb.trap.id = #trap_counter {ns}.data
execute store result score @n[tag=_trap_new_i] {ns}.zb.trap.price run data get storage {ns}:temp _trap_iter[0].price
execute store result score @n[tag=_trap_new_i] {ns}.zb.trap.power run data get storage {ns}:temp _trap_iter[0].power
tag @e[tag=_trap_new_i] remove _trap_new_i

# Set scoreboards on marker entity
scoreboard players operation @n[tag=_trap_new_m] {ns}.zb.trap.id = #trap_counter {ns}.data
execute store result score @n[tag=_trap_new_m] {ns}.zb.trap.type run data get storage {ns}:temp _trap_iter[0].type
execute store result score @n[tag=_trap_new_m] {ns}.zb.trap.dur run data get storage {ns}:temp _trap_iter[0].duration
execute store result score @n[tag=_trap_new_m] {ns}.zb.trap.cd_max run data get storage {ns}:temp _trap_iter[0].cooldown
scoreboard players set @n[tag=_trap_new_m] {ns}.zb.trap.timer 0
scoreboard players set @n[tag=_trap_new_m] {ns}.zb.trap.cd 0

# Compute max radius from effect_radius
execute store result score #tr_x {ns}.data run data get storage {ns}:temp _trap_iter[0].effect_radius[0]
execute store result score #tr_y {ns}.data run data get storage {ns}:temp _trap_iter[0].effect_radius[1]
execute store result score #tr_z {ns}.data run data get storage {ns}:temp _trap_iter[0].effect_radius[2]
scoreboard players operation #tr_max {ns}.data = #tr_x {ns}.data
execute if score #tr_y {ns}.data > #tr_max {ns}.data run scoreboard players operation #tr_max {ns}.data = #tr_y {ns}.data
execute if score #tr_z {ns}.data > #tr_max {ns}.data run scoreboard players operation #tr_max {ns}.data = #tr_z {ns}.data
scoreboard players operation @n[tag=_trap_new_m] {ns}.zb.trap.radius = #tr_max {ns}.data
tag @e[tag=_trap_new_m] remove _trap_new_m

# Register Bookshelf events on interaction entity
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/traps/on_right_click",executor:"source"}}
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_hover_enter {{run:"function {ns}:v{version}/zombies/traps/on_hover_enter",executor:"source"}}
execute as @e[tag=_trap_new_bs] run function #bs.interaction:on_hover_leave {{run:"function {ns}:v{version}/zombies/traps/on_hover_leave",executor:"source"}}
tag @e[tag=_trap_new_bs] remove _trap_new_bs

# Continue iteration
data remove storage {ns}:temp _trap_iter[0]
execute if data storage {ns}:temp _trap_iter[0] run function {ns}:v{version}/zombies/traps/setup_iter
""")

	write_versioned_function("zombies/traps/place_at", f"""
# Summon interaction entity at offset position
$summon minecraft:interaction $(ix) $(iy) $(iz) {{width:1.0f,height:1.0f,response:true,Tags:["{ns}.trap_interact","{ns}.gm_entity","bs.entity.interaction","_trap_new_i","_trap_new_bs"]}}

# Summon marker entity at trap center
$summon minecraft:marker $(cx) $(cy) $(cz) {{Tags:["{ns}.trap_center","{ns}.gm_entity","_trap_new_m"]}}
""")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/traps/on_right_click", f"""
# Guard: game must be active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Check power requirement
execute store result score #trap_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.power
execute if score #trap_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":" ⚡ Requires power!","color":"red"}}]

# Get trap ID
execute store result score #trap_id {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.id

# Check if trap is ready (not active, not on cooldown)
scoreboard players set #trap_ready {ns}.data 0
execute as @e[tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data if score @s {ns}.zb.trap.timer matches 0 if score @s {ns}.zb.trap.cd matches 0 run scoreboard players set #trap_ready {ns}.data 1
execute unless score #trap_ready {ns}.data matches 1 run return run tellraw @s [{MGS_TAG},{{"text":" Trap not ready!","color":"yellow"}}]

# Check price
execute store result score #trap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.price
execute unless score @s {ns}.zb.points >= #trap_price {ns}.data run return run tellraw @s [{MGS_TAG},{{"text":" Not enough points!","color":"red"}}]

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #trap_price {ns}.data

# Activate trap (set timer = duration on the marker)
execute as @e[tag={ns}.trap_center] if score @s {ns}.zb.trap.id = #trap_id {ns}.data run scoreboard players operation @s {ns}.zb.trap.timer = @s {ns}.zb.trap.dur

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":" ⚠ Trap activated!","color":"gold"}}]
""")

	## Active trap tick: damage zombies, particles, decrement timer
	write_versioned_function("zombies/traps/active_tick", f"""
# @s = trap center marker, at @s position

# Apply damage based on trap type
execute store result storage {ns}:temp _trap_tick.r int 1 run scoreboard players get @s {ns}.zb.trap.radius
execute if score @s {ns}.zb.trap.type matches 0 run function {ns}:v{version}/zombies/traps/damage_fire with storage {ns}:temp _trap_tick
execute if score @s {ns}.zb.trap.type matches 1 run function {ns}:v{version}/zombies/traps/damage_electric with storage {ns}:temp _trap_tick

# Particles based on type
execute if score @s {ns}.zb.trap.type matches 0 run particle minecraft:flame ~ ~1 ~ 1.5 0.5 1.5 0.05 10
execute if score @s {ns}.zb.trap.type matches 1 run particle minecraft:electric_spark ~ ~1 ~ 1.5 0.5 1.5 0.1 15

# Decrement timer
scoreboard players remove @s {ns}.zb.trap.timer 1

# Check if deactivated
execute if score @s {ns}.zb.trap.timer matches 0 run scoreboard players operation @s {ns}.zb.trap.cd = @s {ns}.zb.trap.cd_max
""")

	write_versioned_function("zombies/traps/damage_fire", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(r)] run damage @s 5 minecraft:on_fire
""")

	write_versioned_function("zombies/traps/damage_electric", f"""
$execute as @e[tag={ns}.zombie_round,distance=..$(r)] run damage @s 99999
""")

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/traps/on_hover_enter", f"""
execute store result score #trap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.trap.price
title @s times 0 40 10
title @s title [{{"text":"⚠ Trap","color":"red"}}]
title @s subtitle [{{"text":"Cost: ","color":"gray"}},{{"score":{{"name":"#trap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}]
""")

	write_versioned_function("zombies/traps/on_hover_leave", """
title @s clear
""")

	## Hook into game tick: process active traps and cooldowns
	write_versioned_function("zombies/game_tick", f"""
# Trap active tick (damage + timer)
execute as @e[tag={ns}.trap_center,scores={{{ns}.zb.trap.timer=1..}}] at @s run function {ns}:v{version}/zombies/traps/active_tick

# Trap cooldown tick
execute as @e[tag={ns}.trap_center,scores={{{ns}.zb.trap.cd=1..}}] run scoreboard players remove @s {ns}.zb.trap.cd 1
""")

	## Hook into preload_complete: setup traps
	write_versioned_function("zombies/preload_complete", f"""
# Setup traps
execute if data storage {ns}:zombies game.map.traps[0] run function {ns}:v{version}/zombies/traps/setup
""")
