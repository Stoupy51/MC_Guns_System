
#> mgs:v5.4.4/lobby/multiplayer/speed_up
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/vote_tick
#

scoreboard players set #lv_mp_timer mgs.data 100
execute as @a[scores={mgs.lobby.queue=1}] at @s run playsound minecraft:entity.villager.celebrate ambient @s
tellraw @a[scores={mgs.lobby.queue=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.everyone_has_voted_the_vote_ends_in_5_seconds","fallback":"Everyone has voted, the vote ends in 5 seconds!","color":"aqua"}]

