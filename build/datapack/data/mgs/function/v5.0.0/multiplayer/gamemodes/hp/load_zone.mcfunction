
#> mgs:v5.0.0/multiplayer/gamemodes/hp/load_zone
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/hp/setup
#			mgs:v5.0.0/multiplayer/gamemodes/hp/rotate
#

# Kill old zone marker
kill @e[tag=mgs.hp_marker]
kill @e[tag=mgs.hp_label]

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

# Assign point label (fallback to HP for maps with >5 zones)
data modify storage mgs:temp _hp_pos.label set value "HP"
execute if score #hp_zone_idx mgs.data matches 0 run data modify storage mgs:temp _hp_pos.label set value "A"
execute if score #hp_zone_idx mgs.data matches 1 run data modify storage mgs:temp _hp_pos.label set value "B"
execute if score #hp_zone_idx mgs.data matches 2 run data modify storage mgs:temp _hp_pos.label set value "C"
execute if score #hp_zone_idx mgs.data matches 3 run data modify storage mgs:temp _hp_pos.label set value "D"
execute if score #hp_zone_idx mgs.data matches 4 run data modify storage mgs:temp _hp_pos.label set value "E"
scoreboard players add #hp_zone_idx mgs.data 1

function mgs:v5.0.0/multiplayer/gamemodes/hp/summon_marker with storage mgs:temp _hp_pos

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"⚡ ","color":"dark_purple"}, {"translate":"mgs.hardpoint_2"}],{"storage":"mgs:temp","nbt":"_hp_pos.label","color":"yellow","interpret":true},[{"text":" ","color":"dark_purple"}, {"translate":"mgs.active"}]]
playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1 1.0

