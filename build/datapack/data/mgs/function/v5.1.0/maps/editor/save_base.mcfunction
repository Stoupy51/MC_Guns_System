
#> mgs:v5.1.0/maps/editor/save_base
#
# @executed	at @s
#
# @within	mgs:v5.1.0/maps/editor/do_save [ at @s ]
#

# Run as the base marker, at it.
execute store result storage mgs:temp map_edit.map.base_coordinates[0] int 1 run data get entity @s Pos[0]
execute store result storage mgs:temp map_edit.map.base_coordinates[1] int 1 run data get entity @s Pos[1]
execute store result storage mgs:temp map_edit.map.base_coordinates[2] int 1 run data get entity @s Pos[2]

# Only written when set on the marker.
execute if data entity @s data.start_function run data modify storage mgs:temp map_edit.map.start_function set from entity @s data.start_function
execute unless data entity @s data.start_function run data remove storage mgs:temp map_edit.map.start_function
execute if data entity @s data.tick_function run data modify storage mgs:temp map_edit.map.tick_function set from entity @s data.tick_function
execute unless data entity @s data.tick_function run data remove storage mgs:temp map_edit.map.tick_function

