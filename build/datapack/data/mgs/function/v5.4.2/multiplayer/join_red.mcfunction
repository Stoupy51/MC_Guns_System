
#> mgs:v5.4.2/multiplayer/join_red
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/auto_assign_team
#			dialog mgs:v5.4.2/multiplayer/setup
#

scoreboard players set @s mgs.mp.team 1
scoreboard players set @s mgs.mp.in_game 1
team join mgs.red @s
tellraw @s ["",{"translate":"mgs.you_joined","fallback":"You joined ","color":"white"},{"translate":"mgs.red_team","fallback":"Red Team","color":"red","bold":true}]

