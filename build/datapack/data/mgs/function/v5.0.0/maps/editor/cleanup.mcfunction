
#> mgs:v5.0.0/maps/editor/cleanup
#
# @executed	as @p[tag=mgs.map_editor]
#
# @within	mgs:v5.0.0/maps/editor/save_exit
#			mgs:v5.0.0/maps/editor/exit
#

# Kill all editor markers
kill @e[tag=mgs.map_element]

# Reset editor state
scoreboard players set @s mgs.mp.map_edit 0
tag @s remove mgs.map_editor

# Clear editor tools
clear @s

