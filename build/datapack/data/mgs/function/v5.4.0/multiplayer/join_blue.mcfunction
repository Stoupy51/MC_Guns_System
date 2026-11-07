
#> mgs:v5.4.0/multiplayer/join_blue
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/auto_assign_team
#			dialog mgs:v5.4.0/multiplayer/setup
#

scoreboard players set @s mgs.mp.team 2
scoreboard players set @s mgs.mp.in_game 1
team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.you_joined","fallback":"You joined ","color":"white"},{"translate":"mgs.blue_team","fallback":"Blue Team","color":"blue","bold":true}]

