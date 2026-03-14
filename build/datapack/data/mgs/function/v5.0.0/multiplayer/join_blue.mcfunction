
#> mgs:v5.0.0/multiplayer/join_blue
#
# @within	mgs:v5.0.0/multiplayer/auto_assign_team
#

scoreboard players set @s mgs.mp.team 2
team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.you_joined","color":"white"},{"translate":"mgs.blue_team","color":"blue","bold":true}]

