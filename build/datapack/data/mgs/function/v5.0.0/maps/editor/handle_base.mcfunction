
#> mgs:v5.0.0/maps/editor/handle_base
#
# @executed	as @e[tag=mgs.new_element,limit=1,sort=nearest] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Kill any existing base marker
kill @e[tag=mgs.map_element,tag=mgs.element.base_coordinates]

# Get position
execute store result score #base_x mgs.data run data get entity @s Pos[0]
execute store result score #base_y mgs.data run data get entity @s Pos[1]
execute store result score #base_z mgs.data run data get entity @s Pos[2]

# Summon permanent marker
execute store result storage mgs:temp _pos.x double 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _pos.y double 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _pos.z double 1 run scoreboard players get #base_z mgs.data
function mgs:v5.0.0/maps/editor/summon_base_marker with storage mgs:temp _pos

# Announce
execute as @a[tag=mgs.map_editor] run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.base_coordinates_set","color":"light_purple"}]

