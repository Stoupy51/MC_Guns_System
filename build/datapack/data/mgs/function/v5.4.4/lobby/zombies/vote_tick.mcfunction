
#> mgs:v5.4.4/lobby/zombies/vote_tick
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/tick
#

scoreboard players enable @a[scores={mgs.lobby.queue=2}] mgs.lobby.vote
execute as @a[scores={mgs.lobby.queue=2,mgs.lobby.vote=1..}] run function mgs:v5.4.4/lobby/zombies/read_vote

execute if score #lv_zb_round mgs.data matches 1 if score #lv_zb_voters mgs.data matches 1.. run scoreboard players remove #lv_zb_timer mgs.data 1
execute if score #lv_zb_round mgs.data matches 2 run scoreboard players remove #lv_zb_timer mgs.data 1
execute if score #lv_zb_timer mgs.data matches 101.. if score #lv_zb_voters mgs.data >= #lv_zb_count mgs.data run function mgs:v5.4.4/lobby/zombies/speed_up
execute if score #lv_zb_timer mgs.data matches ..0 run function mgs:v5.4.4/lobby/zombies/resolve

