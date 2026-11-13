
#> mgs:v5.4.2/zombies/save/find_player
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/enlist_player
#			mgs:v5.4.2/zombies/save/restore_player
#

data remove storage mgs:temp _sv_player
data modify storage mgs:temp _sv_find set from storage mgs:zombies_saves loading.players
execute if data storage mgs:temp _sv_find[0] run function mgs:v5.4.2/zombies/save/find_player_next
data remove storage mgs:temp _sv_find

