
#> mgs:v5.0.0/multiplayer/gamemodes/hp/load_zone
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/hp/setup
#			mgs:v5.0.0/multiplayer/gamemodes/hp/rotate
#

# Kill old zone markers
kill @e[tag=mgs.hp_corner]

# Corner A: relative → absolute
execute store result score #_rx mgs.data run data get storage mgs:multiplayer game.hp_zones[0][0]
execute store result score #_ry mgs.data run data get storage mgs:multiplayer game.hp_zones[0][1]
execute store result score #_rz mgs.data run data get storage mgs:multiplayer game.hp_zones[0][2]
scoreboard players operation #_rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #_rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _hp_pos.x double 1 run scoreboard players get #_rx mgs.data
execute store result storage mgs:temp _hp_pos.y double 1 run scoreboard players get #_ry mgs.data
execute store result storage mgs:temp _hp_pos.z double 1 run scoreboard players get #_rz mgs.data
function mgs:v5.0.0/multiplayer/gamemodes/hp/summon_corner_a with storage mgs:temp _hp_pos

# Corner B: relative → absolute
execute if data storage mgs:multiplayer game.hp_zones[1] store result score #_rx mgs.data run data get storage mgs:multiplayer game.hp_zones[1][0]
execute if data storage mgs:multiplayer game.hp_zones[1] store result score #_ry mgs.data run data get storage mgs:multiplayer game.hp_zones[1][1]
execute if data storage mgs:multiplayer game.hp_zones[1] store result score #_rz mgs.data run data get storage mgs:multiplayer game.hp_zones[1][2]
scoreboard players operation #_rx mgs.data += #gm_base_x mgs.data
scoreboard players operation #_ry mgs.data += #gm_base_y mgs.data
scoreboard players operation #_rz mgs.data += #gm_base_z mgs.data
execute store result storage mgs:temp _hp_pos.x double 1 run scoreboard players get #_rx mgs.data
execute store result storage mgs:temp _hp_pos.y double 1 run scoreboard players get #_ry mgs.data
execute store result storage mgs:temp _hp_pos.z double 1 run scoreboard players get #_rz mgs.data
execute if data storage mgs:multiplayer game.hp_zones[1] run function mgs:v5.0.0/multiplayer/gamemodes/hp/summon_corner_b with storage mgs:temp _hp_pos

tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.hardpoint_zone_active","color":"dark_purple"}]
playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1 1.0

