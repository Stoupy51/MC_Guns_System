
#> mgs:v5.0.0/multiplayer/gamemodes/snd/summon_obj
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/setup
#			mgs:v5.0.0/multiplayer/gamemodes/snd/summon_obj
#

execute store result score #_rx mgs.data run data get storage mgs:temp _snd_iter[0][0]
execute store result score #_ry mgs.data run data get storage mgs:temp _snd_iter[0][1]
execute store result score #_rz mgs.data run data get storage mgs:temp _snd_iter[0][2]
scoreboard players operation #_rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #_rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _snd_pos.x double 1 run scoreboard players get #_rx mgs.data
execute store result storage mgs:temp _snd_pos.y double 1 run scoreboard players get #_ry mgs.data
execute store result storage mgs:temp _snd_pos.z double 1 run scoreboard players get #_rz mgs.data
function mgs:v5.0.0/multiplayer/gamemodes/snd/summon_obj_at with storage mgs:temp _snd_pos
data remove storage mgs:temp _snd_iter[0]
execute if data storage mgs:temp _snd_iter[0] run function mgs:v5.0.0/multiplayer/gamemodes/snd/summon_obj

