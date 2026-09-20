
#> mgs:v5.1.0/maps/editor/handle_spawn
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.1.0/maps/editor/process_element
#

# Get position for the permanent marker
execute store result storage mgs:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag from entity
execute if entity @s[tag=mgs.element.red_spawn] run data modify storage mgs:temp _pos.tag set value "mgs.element.red_spawn"
execute if entity @s[tag=mgs.element.blue_spawn] run data modify storage mgs:temp _pos.tag set value "mgs.element.blue_spawn"
execute if entity @s[tag=mgs.element.general_spawn] run data modify storage mgs:temp _pos.tag set value "mgs.element.general_spawn"
execute if entity @s[tag=mgs.element.mission_spawn] run data modify storage mgs:temp _pos.tag set value "mgs.element.mission_spawn"

# Summon permanent marker
function mgs:v5.1.0/maps/editor/summon_spawn_marker with storage mgs:temp _pos

# Get player rotation and snap to nearest 45 degrees
execute store result score #yaw mgs.data run data get entity @p[tag=mgs.map_editor,distance=..6,sort=nearest] Rotation[0]
scoreboard players add #yaw mgs.data 742
scoreboard players operation #yaw mgs.data /= #45 mgs.data
scoreboard players operation #yaw mgs.data *= #45 mgs.data
scoreboard players remove #yaw mgs.data 720
execute as @n[tag=mgs.new_spawn_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw mgs.data
tag @n[tag=mgs.new_spawn_marker] remove mgs.new_spawn_marker

# Announce
execute if entity @s[tag=mgs.element.red_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red_spawn_placed","color":"red"}]
execute if entity @s[tag=mgs.element.blue_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue_spawn_placed","color":"blue"}]
execute if entity @s[tag=mgs.element.general_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.general_spawn_placed","color":"yellow"}]
execute if entity @s[tag=mgs.element.mission_spawn] run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_spawn_placed","color":"aqua"}]

