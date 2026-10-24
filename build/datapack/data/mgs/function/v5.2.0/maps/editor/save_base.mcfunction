
#> mgs:v5.2.0/maps/editor/save_base
#
# @executed	at @s
#
# @within	mgs:v5.2.0/maps/editor/do_save [ at @s ]
#

# Run as the base marker, at it.
execute store result storage mgs:temp map_edit.map.base_coordinates[0] int 1 run data get entity @s Pos[0]
execute store result storage mgs:temp map_edit.map.base_coordinates[1] int 1 run data get entity @s Pos[1]
execute store result storage mgs:temp map_edit.map.base_coordinates[2] int 1 run data get entity @s Pos[2]

# Only written when set on the marker.
execute if data entity @s data.start_command run data modify storage mgs:temp map_edit.map.start_command set from entity @s data.start_command
execute unless data entity @s data.start_command run data remove storage mgs:temp map_edit.map.start_command
execute if data entity @s data.tick_command run data modify storage mgs:temp map_edit.map.tick_command set from entity @s data.tick_command
execute unless data entity @s data.tick_command run data remove storage mgs:temp map_edit.map.tick_command

