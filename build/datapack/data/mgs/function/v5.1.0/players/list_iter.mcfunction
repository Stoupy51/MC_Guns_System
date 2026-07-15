
#> mgs:v5.1.0/players/list_iter
#
# @within	mgs:v5.1.0/players/list_iter
#			mgs:v5.1.0/players/list_multiplayer
#			mgs:v5.1.0/players/list_zombies
#			mgs:v5.1.0/players/list_missions
#

execute unless data storage mgs:temp _plr_iter[0] run return fail

# Inject the mode into the first entry for the macro
data modify storage mgs:temp _plr_entry set from storage mgs:temp _plr_iter[0]
data modify storage mgs:temp _plr_entry.mode set from storage mgs:temp _plr_mode

# Append one button for this player
function mgs:v5.1.0/players/list_entry with storage mgs:temp _plr_entry

# Advance
data remove storage mgs:temp _plr_iter[0]
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.1.0/players/list_iter

