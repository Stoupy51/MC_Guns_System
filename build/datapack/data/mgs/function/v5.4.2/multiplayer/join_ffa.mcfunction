
#> mgs:v5.4.2/multiplayer/join_ffa
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/auto_assign_team
#

scoreboard players set @s mgs.mp.team 0
scoreboard players set @s mgs.mp.in_game 1
team join mgs.ffa @s
tellraw @s ["",{"translate":"mgs.you_joined_the","fallback":"You joined the ","color":"white"},{"translate":"mgs.free_for_all","fallback":"Free For All","color":"yellow","bold":true}]

