
#> mgs:v5.4.4/lobby/missions/join
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/player/config/process
#

execute unless score #public_lobby mgs.config matches 1 run return fail
execute if score @s mgs.lobby.queue matches 3 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_are_already_in_the_missions_queue","fallback":"You are already in the Missions queue.","color":"yellow"}]

function mgs:v5.4.4/lobby/leave_games
scoreboard players set @s mgs.lobby.queue 3
scoreboard players set @s mgs.lobby.choice 0
scoreboard players set @s mgs.lobby.vote 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_joined_the_missions_queue","fallback":"You joined the Missions queue.","color":"green"}]
execute if score #lv_mi_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/missions/message

