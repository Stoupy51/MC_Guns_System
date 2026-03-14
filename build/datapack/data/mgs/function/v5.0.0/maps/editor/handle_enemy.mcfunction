
#> mgs:v5.0.0/maps/editor/handle_enemy
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Initialize default function if missing
execute unless data storage mgs:temp map_edit.map.default_enemy_function run data modify storage mgs:temp map_edit.map.default_enemy_function set value "mgs:v5.0.0/mob/default/level_1 {\"entity\":\"pillager\"}"

# Get position for permanent marker
execute store result storage mgs:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function mgs:v5.0.0/maps/editor/summon_enemy_marker with storage mgs:temp _pos

# Store the default function on the marker
execute as @n[tag=mgs.new_enemy_marker] run data modify entity @s data.function set from storage mgs:temp map_edit.map.default_enemy_function
tag @e[tag=mgs.new_enemy_marker] remove mgs.new_enemy_marker

# Announce
tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.enemy_placed","color":"red"}]

