
#> mgs:v5.1.0/maps/editor/menu_entry
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/maps/editor/list/multiplayer
#			mgs:v5.1.0/maps/editor/list/zombies
#			mgs:v5.1.0/maps/editor/list/missions
#			mgs:v5.1.0/maps/editor/menu_entry
#

data modify storage mgs:temp map_menu.current set from storage mgs:temp map_menu.list[0]

# Flattened for the macro.
data modify storage mgs:temp map_menu.name set from storage mgs:temp map_menu.current.name
data modify storage mgs:temp map_menu.id set from storage mgs:temp map_menu.current.id

execute store result storage mgs:temp map_menu.idx int 1 run scoreboard players get #map_menu_idx mgs.data

function mgs:v5.1.0/maps/editor/menu_entry_display with storage mgs:temp map_menu

data remove storage mgs:temp map_menu.list[0]
scoreboard players add #map_menu_idx mgs.data 1
execute if data storage mgs:temp map_menu.list[0] run function mgs:v5.1.0/maps/editor/menu_entry

