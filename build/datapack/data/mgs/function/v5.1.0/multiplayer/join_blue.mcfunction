
#> mgs:v5.1.0/multiplayer/join_blue
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/auto_assign_team
#			dialog mgs:v5.1.0/multiplayer/setup
#

scoreboard players set @s mgs.mp.team 2
scoreboard players set @s mgs.mp.in_game 1
team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.you_joined","color":"white"},{"translate":"mgs.blue_team","color":"blue","bold":true}]

