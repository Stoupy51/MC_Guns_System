
#> mgs:v5.4.0/maps/editor/session_check
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/do_save [ as @e[type=minecraft:marker,tag=mgs.map_element] ]
#			mgs:v5.4.0/maps/editor/sweep [ as @e[type=minecraft:marker,tag=mgs.map_element] ]
#			mgs:v5.4.0/maps/editor/sweep [ as @e[type=minecraft:item_display,tag=mgs.editor_display] ]
#			mgs:v5.4.0/maps/editor/sweep [ as @e[type=minecraft:block_display,tag=mgs.editor_display] ]
#

execute unless score @s mgs.ed.session matches -2147483648.. run return run scoreboard players operation @s mgs.ed.session = #ed_session mgs.data
execute unless score @s mgs.ed.session = #ed_session mgs.data run kill @s

