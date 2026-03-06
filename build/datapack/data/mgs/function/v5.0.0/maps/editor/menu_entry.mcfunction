
#> mgs:v5.0.0/maps/editor/menu_entry
#
# @within	mgs:v5.0.0/maps/editor/list/multiplayer
#			mgs:v5.0.0/maps/editor/list/zombies
#			mgs:v5.0.0/maps/editor/list/missions
#			mgs:v5.0.0/maps/editor/menu_entry
#

# Read current map name and id
data modify storage mgs:temp map_menu.current set from storage mgs:temp map_menu.list[0]

# Flatten fields for macro
data modify storage mgs:temp map_menu.name set from storage mgs:temp map_menu.current.name
data modify storage mgs:temp map_menu.id set from storage mgs:temp map_menu.current.id

# Store current index for macro
execute store result storage mgs:temp map_menu.idx int 1 run scoreboard players get #map_menu_idx mgs.data

# Display the entry using macro
function mgs:v5.0.0/maps/editor/menu_entry_display with storage mgs:temp map_menu

# Advance to next
data remove storage mgs:temp map_menu.list[0]
scoreboard players add #map_menu_idx mgs.data 1
execute if data storage mgs:temp map_menu.list[0] run function mgs:v5.0.0/maps/editor/menu_entry

