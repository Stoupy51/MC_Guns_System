
#> mgs:v5.4.4/lobby/missions/second
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/second
#

execute store result score #lv_mi_count mgs.data if entity @a[scores={mgs.lobby.queue=3}]
execute if data storage mgs:missions game{state:"active"} as @a[scores={mgs.lobby.queue=3}] unless score @s mgs.mi.in_game matches 1 run function mgs:v5.4.4/missions/join_game

execute if score #lv_mi_round mgs.data matches 1.. unless score #lv_mi_count mgs.data matches 1.. run function mgs:v5.4.4/lobby/missions/cancel_vote
execute unless score #lv_mi_round mgs.data matches 1.. if score #lv_mi_count mgs.data matches 1.. if data storage mgs:missions game{state:"lobby"} run function mgs:v5.4.4/lobby/missions/open_vote
execute if score #lv_mi_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/missions/vote_second

# A game nobody is online in waits 10 minutes for them, then frees the mode.
execute unless entity @a[scores={mgs.mi.in_game=1}] unless data storage mgs:missions game{state:"lobby"} run scoreboard players add #lv_mi_empty mgs.data 1
execute if entity @a[scores={mgs.mi.in_game=1}] run scoreboard players set #lv_mi_empty mgs.data 0
execute if data storage mgs:missions game{state:"lobby"} run scoreboard players set #lv_mi_empty mgs.data 0
execute if score #lv_mi_empty mgs.data matches 600.. run function mgs:v5.4.4/missions/stop

