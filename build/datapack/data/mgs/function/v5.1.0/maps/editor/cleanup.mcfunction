
#> mgs:v5.1.0/maps/editor/cleanup
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	mgs:v5.1.0/maps/editor/save_exit
#			mgs:v5.1.0/maps/editor/exit
#

# Kill all editor markers and model displays
kill @e[tag=mgs.map_element]
kill @e[tag=mgs.editor_display]

# Reset editor state
scoreboard players set @s mgs.mp.map_edit 0
tag @s remove mgs.map_editor

# Clear editor tools
clear @s

