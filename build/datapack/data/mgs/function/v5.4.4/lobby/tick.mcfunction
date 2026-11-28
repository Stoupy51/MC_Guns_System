
#> mgs:v5.4.4/lobby/tick
#
# @within	mgs:v5.4.4/tick
#			mgs:v5.4.4/dialog/close_then
#

execute if score #lv_mp_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/multiplayer/vote_tick
execute if score #lv_zb_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/zombies/vote_tick
execute if score #lv_mi_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/missions/vote_tick
scoreboard players add #lv_tick mgs.data 1
execute if score #lv_tick mgs.data matches 20.. run function mgs:v5.4.4/lobby/second

