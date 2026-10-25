
#> mgs:v5.3.0/maps/editor/handle_base
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.3.0/maps/editor/process_element
#

# start_command and tick_command survive the move.
execute if data entity @n[tag=mgs.element.base_coordinates] data.start_command run data modify storage mgs:temp _base_preserve.start_command set from entity @n[tag=mgs.element.base_coordinates] data.start_command
execute if data entity @n[tag=mgs.element.base_coordinates] data.tick_command run data modify storage mgs:temp _base_preserve.tick_command set from entity @n[tag=mgs.element.base_coordinates] data.tick_command

kill @e[tag=mgs.element.base_coordinates]

execute store result score #base_x mgs.data run data get entity @s Pos[0]
execute store result score #base_y mgs.data run data get entity @s Pos[1]
execute store result score #base_z mgs.data run data get entity @s Pos[2]

execute store result storage mgs:temp _pos.x double 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _pos.y double 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _pos.z double 1 run scoreboard players get #base_z mgs.data
function mgs:v5.3.0/maps/editor/summon_base_marker with storage mgs:temp _pos

execute if data storage mgs:temp _base_preserve.start_command run data modify entity @n[tag=mgs.element.base_coordinates] data.start_command set from storage mgs:temp _base_preserve.start_command
execute if data storage mgs:temp _base_preserve.tick_command run data modify entity @n[tag=mgs.element.base_coordinates] data.tick_command set from storage mgs:temp _base_preserve.tick_command
data remove storage mgs:temp _base_preserve

execute as @a[tag=mgs.map_editor] run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.base_coordinates_set","fallback":"Base coordinates set!","color":"light_purple"}]

