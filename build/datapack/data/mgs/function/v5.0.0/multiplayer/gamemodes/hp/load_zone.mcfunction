
#> mgs:v5.0.0/multiplayer/gamemodes/hp/load_zone
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/hp/setup
#			mgs:v5.0.0/multiplayer/gamemodes/hp/rotate
#

# Kill old zone marker
kill @e[tag=mgs.hp_marker]

# Zone point: relative → absolute
execute store result score #rx mgs.data run data get storage mgs:multiplayer game.hp_zones[0][0]
execute store result score #ry mgs.data run data get storage mgs:multiplayer game.hp_zones[0][1]
execute store result score #rz mgs.data run data get storage mgs:multiplayer game.hp_zones[0][2]
scoreboard players operation #rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _hp_pos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _hp_pos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _hp_pos.z double 1 run scoreboard players get #rz mgs.data
function mgs:v5.0.0/multiplayer/gamemodes/hp/summon_marker with storage mgs:temp _hp_pos

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"⚡ ","color":"dark_purple"}, {"translate":"mgs.hardpoint_zone_active"}]]
playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1 1.0

