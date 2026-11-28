
#> mgs:v5.4.4/lobby/missions/vote_tick
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/tick
#

scoreboard players enable @a[scores={mgs.lobby.queue=3}] mgs.lobby.vote
execute as @a[scores={mgs.lobby.queue=3,mgs.lobby.vote=1..}] run function mgs:v5.4.4/lobby/missions/read_vote

execute if score #lv_mi_round mgs.data matches 1 if score #lv_mi_voters mgs.data matches 1.. run scoreboard players remove #lv_mi_timer mgs.data 1
execute if score #lv_mi_round mgs.data matches 2 run scoreboard players remove #lv_mi_timer mgs.data 1
execute if score #lv_mi_timer mgs.data matches 101.. if score #lv_mi_voters mgs.data >= #lv_mi_count mgs.data run function mgs:v5.4.4/lobby/missions/speed_up
execute if score #lv_mi_timer mgs.data matches ..0 run function mgs:v5.4.4/lobby/missions/resolve

