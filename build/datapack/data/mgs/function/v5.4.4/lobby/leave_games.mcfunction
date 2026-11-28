
#> mgs:v5.4.4/lobby/leave_games
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/join
#			mgs:v5.4.4/lobby/zombies/join
#			mgs:v5.4.4/lobby/missions/join
#			mgs:v5.4.4/lobby/login
#			mgs:v5.4.4/lobby/send_home
#

scoreboard players set #lv_in_game mgs.data 0
execute if score @s mgs.mp.in_game matches 1 run scoreboard players set #lv_in_game mgs.data 1
execute if score @s mgs.zb.in_game matches 1 run scoreboard players set #lv_in_game mgs.data 1
execute if score @s mgs.mi.in_game matches 1 run scoreboard players set #lv_in_game mgs.data 1
execute if score @s mgs.mp.in_game matches 1 run function mgs:v5.4.4/lobby/multiplayer/leave
execute if score @s mgs.zb.in_game matches 1 run function mgs:v5.4.4/lobby/zombies/leave
execute if score @s mgs.mi.in_game matches 1 run function mgs:v5.4.4/lobby/missions/leave
scoreboard players set @s mgs.lobby.choice 0

