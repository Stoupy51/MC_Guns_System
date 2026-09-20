
#> mgs:v5.1.0/multiplayer/join_ffa
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/auto_assign_team
#

scoreboard players set @s mgs.mp.team 0
scoreboard players set @s mgs.mp.in_game 1
team join mgs.ffa @s
tellraw @s ["",{"translate":"mgs.you_joined_the","color":"white"},{"translate":"mgs.free_for_all","color":"yellow","bold":true}]

