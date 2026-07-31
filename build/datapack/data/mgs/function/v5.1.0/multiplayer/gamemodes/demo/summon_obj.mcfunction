
#> mgs:v5.1.0/multiplayer/gamemodes/demo/summon_obj
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/setup
#			mgs:v5.1.0/multiplayer/gamemodes/demo/summon_obj
#

execute store result score #rx mgs.data run data get storage mgs:temp _demo_iter[0][0]
execute store result score #ry mgs.data run data get storage mgs:temp _demo_iter[0][1]
execute store result score #rz mgs.data run data get storage mgs:temp _demo_iter[0][2]
scoreboard players operation #rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _demo_pos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _demo_pos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _demo_pos.z double 1 run scoreboard players get #rz mgs.data

# Site letter, same scheme as domination's zone labels
execute if score #demo_site_idx mgs.data matches 0 run data modify storage mgs:temp _demo_pos.label set value "A"
execute if score #demo_site_idx mgs.data matches 1 run data modify storage mgs:temp _demo_pos.label set value "B"
execute if score #demo_site_idx mgs.data matches 2 run data modify storage mgs:temp _demo_pos.label set value "C"
execute if score #demo_site_idx mgs.data matches 3 run data modify storage mgs:temp _demo_pos.label set value "D"
scoreboard players add #demo_site_idx mgs.data 1

function mgs:v5.1.0/multiplayer/gamemodes/demo/summon_obj_at with storage mgs:temp _demo_pos
data remove storage mgs:temp _demo_iter[0]
execute if data storage mgs:temp _demo_iter[0] run function mgs:v5.1.0/multiplayer/gamemodes/demo/summon_obj

