
#> mgs:v5.4.4/zombies/save/enlist_player
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/zombies/save/load [ as @a ]
#

function mgs:v5.4.4/zombies/save/find_player
execute if data storage mgs:temp _sv_player run scoreboard players set @s mgs.zb.in_game 1
data remove storage mgs:temp _sv_player

