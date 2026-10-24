
#> mgs:v5.2.0/multiplayer/join_red
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.2.0/multiplayer/auto_assign_team
#			dialog mgs:v5.2.0/multiplayer/setup
#

scoreboard players set @s mgs.mp.team 1
scoreboard players set @s mgs.mp.in_game 1
team join mgs.red @s
tellraw @s ["",{"translate":"mgs.you_joined","fallback":"You joined ","color":"white"},{"translate":"mgs.red_team","fallback":"Red Team","color":"red","bold":true}]

