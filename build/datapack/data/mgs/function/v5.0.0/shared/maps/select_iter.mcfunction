
#> mgs:v5.0.0/shared/maps/select_iter
#
# @within	mgs:v5.0.0/shared/maps/select_iter
#			mgs:v5.0.0/zombies/map_select
#			mgs:v5.0.0/multiplayer/map_select
#			mgs:v5.0.0/missions/map_select
#

execute unless data storage mgs:temp _map_iter[0] run return fail

# Inject mode into the first entry for the macro
data modify storage mgs:temp _map_entry set from storage mgs:temp _map_iter[0]
data modify storage mgs:temp _map_entry.mode set from storage mgs:temp _map_select_mode

# Call shared entry
function mgs:v5.0.0/shared/maps/select_entry with storage mgs:temp _map_entry

# Advance
data remove storage mgs:temp _map_iter[0]
scoreboard players add #map_idx mgs.data 1
execute if data storage mgs:temp _map_iter[0] run function mgs:v5.0.0/shared/maps/select_iter

