
#> mgs:v5.4.4/lobby/zombies/join
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/player/config/process
#

execute unless score #public_lobby mgs.config matches 1 run return fail
execute if score @s mgs.lobby.queue matches 2 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_are_already_in_the_zombies_queue","fallback":"You are already in the Zombies queue.","color":"yellow"}]

function mgs:v5.4.4/lobby/leave_games
scoreboard players set @s mgs.lobby.queue 2
scoreboard players set @s mgs.lobby.choice 0
scoreboard players set @s mgs.lobby.vote 0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_joined_the_zombies_queue","fallback":"You joined the Zombies queue.","color":"green"}]
execute if score #lv_zb_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/zombies/message

