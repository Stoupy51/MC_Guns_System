
#> mgs:v5.4.1/maps/editor/sweep
#
# @within	mgs:v5.4.1/tick
#			mgs:v5.4.1/dialog/close_then
#

execute as @e[type=minecraft:marker,tag=mgs.map_element] run function mgs:v5.4.1/maps/editor/session_check
execute as @e[type=minecraft:item_display,tag=mgs.editor_display] run function mgs:v5.4.1/maps/editor/session_check
execute as @e[type=minecraft:block_display,tag=mgs.editor_display] run function mgs:v5.4.1/maps/editor/session_check

