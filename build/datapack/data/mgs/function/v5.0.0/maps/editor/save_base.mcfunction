
#> mgs:v5.0.0/maps/editor/save_base
#
# @executed	as @n[tag=...] & at @s
#
# @within	mgs:v5.0.0/maps/editor/do_save [ as @n[tag=...] & at @s ]
#

# @s = base_coordinates marker, at its position
execute store result storage mgs:temp map_edit.map.base_coordinates[0] int 1 run data get entity @s Pos[0]
execute store result storage mgs:temp map_edit.map.base_coordinates[1] int 1 run data get entity @s Pos[1]
execute store result storage mgs:temp map_edit.map.base_coordinates[2] int 1 run data get entity @s Pos[2]

