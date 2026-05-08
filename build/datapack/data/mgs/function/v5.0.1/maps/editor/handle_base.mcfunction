
#> mgs:v5.0.1/maps/editor/handle_base
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.1/maps/editor/process_element
#

# Preserve start_function and tick_function from existing base marker
execute if data entity @n[tag=mgs.element.base_coordinates] data.start_function run data modify storage mgs:temp _base_preserve.start_function set from entity @n[tag=mgs.element.base_coordinates] data.start_function
execute if data entity @n[tag=mgs.element.base_coordinates] data.tick_function run data modify storage mgs:temp _base_preserve.tick_function set from entity @n[tag=mgs.element.base_coordinates] data.tick_function

# Kill any existing base marker
kill @e[tag=mgs.element.base_coordinates]

# Get position
execute store result score #base_x mgs.data run data get entity @s Pos[0]
execute store result score #base_y mgs.data run data get entity @s Pos[1]
execute store result score #base_z mgs.data run data get entity @s Pos[2]

# Summon permanent marker
execute store result storage mgs:temp _pos.x double 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _pos.y double 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _pos.z double 1 run scoreboard players get #base_z mgs.data
function mgs:v5.0.1/maps/editor/summon_base_marker with storage mgs:temp _pos

# Restore preserved start_function and tick_function
execute if data storage mgs:temp _base_preserve.start_function run data modify entity @n[tag=mgs.element.base_coordinates] data.start_function set from storage mgs:temp _base_preserve.start_function
execute if data storage mgs:temp _base_preserve.tick_function run data modify entity @n[tag=mgs.element.base_coordinates] data.tick_function set from storage mgs:temp _base_preserve.tick_function
data remove storage mgs:temp _base_preserve

# Announce
execute as @a[tag=mgs.map_editor] run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.base_coordinates_set","color":"light_purple"}]

