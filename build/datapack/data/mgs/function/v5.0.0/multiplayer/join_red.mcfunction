
#> mgs:v5.0.0/multiplayer/join_red
#
# @executed	as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}]
#
# @within	mgs:v5.0.0/multiplayer/auto_assign_team
#

scoreboard players set @s mgs.mp.team 1
team join mgs.red @s
tellraw @s ["",{"translate":"mgs.you_joined","color":"white"},{"translate":"mgs.red_team","color":"red","bold":true}]

