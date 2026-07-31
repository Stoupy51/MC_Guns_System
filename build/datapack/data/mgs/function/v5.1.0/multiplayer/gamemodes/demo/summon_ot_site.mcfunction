
#> mgs:v5.1.0/multiplayer/gamemodes/demo/summon_ot_site
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/start_overtime
#

data remove storage mgs:temp _demo_iter
data modify storage mgs:temp _demo_iter append from storage mgs:multiplayer game.map.domination[1]
execute unless data storage mgs:temp _demo_iter[0] run data modify storage mgs:temp _demo_iter append from storage mgs:multiplayer game.map.search_and_destroy[0]
execute unless data storage mgs:temp _demo_iter[0] run return fail

execute store result score #rx mgs.data run data get storage mgs:temp _demo_iter[0][0]
execute store result score #ry mgs.data run data get storage mgs:temp _demo_iter[0][1]
execute store result score #rz mgs.data run data get storage mgs:temp _demo_iter[0][2]
scoreboard players operation #rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _demo_pos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _demo_pos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _demo_pos.z double 1 run scoreboard players get #rz mgs.data
data modify storage mgs:temp _demo_pos.label set value "OT"
function mgs:v5.1.0/multiplayer/gamemodes/demo/summon_obj_at with storage mgs:temp _demo_pos

scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_state 0
scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_prog 0
scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_fuse 0
scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_owner 0

