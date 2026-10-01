
#> mgs:v5.1.0/zombies/barricades/setup_iter
#
# @within	mgs:v5.1.0/zombies/barricades/setup
#			mgs:v5.1.0/zombies/barricades/setup_iter
#

scoreboard players add #barricade_counter mgs.data 1

execute store result score #bx mgs.data run data get storage mgs:temp _barricade_iter[0].pos[0]
execute store result score #by mgs.data run data get storage mgs:temp _barricade_iter[0].pos[1]
execute store result score #bz mgs.data run data get storage mgs:temp _barricade_iter[0].pos[2]
scoreboard players operation #bx mgs.data += #gm_base_x mgs.data
scoreboard players operation #by mgs.data += #gm_base_y mgs.data
scoreboard players operation #bz mgs.data += #gm_base_z mgs.data

# Float to score x100 to double x0.01.
execute store result score #byaw mgs.data run data get storage mgs:temp _barricade_iter[0].rotation[0] 100

execute store result storage mgs:temp _bplace.x double 1 run scoreboard players get #bx mgs.data
execute store result storage mgs:temp _bplace.y double 1 run scoreboard players get #by mgs.data
execute store result storage mgs:temp _bplace.z double 1 run scoreboard players get #bz mgs.data
execute store result storage mgs:temp _bplace.yaw double 0.01 run scoreboard players get #byaw mgs.data

function mgs:v5.1.0/zombies/barricades/place_at with storage mgs:temp _bplace

# All zb_object data (block_enabled, block_disabled, radius, ...).
execute as @n[tag=mgs._barricade_new_d] run data modify entity @s data set from storage mgs:temp _barricade_iter[0]

# Fill the blocks a map leaves out at their default, and upgrade pre-26.3 block states.
execute as @n[tag=mgs._barricade_new_d] run function mgs:v5.1.0/maps/light_fields/barricade

execute as @n[tag=mgs._barricade_new_d] run data modify entity @s block_state set from entity @s data.block_enabled

scoreboard players operation @n[tag=mgs._barricade_new_d] mgs.zb.barricade.id = #barricade_counter mgs.data
execute store result score @n[tag=mgs._barricade_new_d] mgs.zb.barricade.radius run data get storage mgs:temp _barricade_iter[0].radius
scoreboard players set @n[tag=mgs._barricade_new_d] mgs.zb.barricade.state 0
scoreboard players set @n[tag=mgs._barricade_new_d] mgs.zb.barricade.r_timer 0
scoreboard players set @n[tag=mgs._barricade_new_d] mgs.zb.barricade.rp_timer 0

execute as @n[tag=mgs._barricade_new_d] at @s run function mgs:v5.1.0/zombies/barricades/compute_brightness

tag @e[tag=mgs._barricade_new_d] remove mgs._barricade_new_d

data remove storage mgs:temp _barricade_iter[0]
execute if data storage mgs:temp _barricade_iter[0] run function mgs:v5.1.0/zombies/barricades/setup_iter

