
#> mgs:v5.4.2/zombies/save/find_player_next
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/find_player
#			mgs:v5.4.2/zombies/save/find_player_next
#

data modify storage mgs:temp _sv_uuid set from entity @s UUID
execute store success score #sv_differs mgs.data run data modify storage mgs:temp _sv_uuid set from storage mgs:temp _sv_find[0].uuid
execute if score #sv_differs mgs.data matches 0 run return run data modify storage mgs:temp _sv_player set from storage mgs:temp _sv_find[0]

data remove storage mgs:temp _sv_find[0]
execute if data storage mgs:temp _sv_find[0] run function mgs:v5.4.2/zombies/save/find_player_next

