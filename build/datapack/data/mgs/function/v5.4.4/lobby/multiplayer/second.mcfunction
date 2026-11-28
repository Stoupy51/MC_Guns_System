
#> mgs:v5.4.4/lobby/multiplayer/second
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/second
#

execute store result score #lv_mp_count mgs.data if entity @a[scores={mgs.lobby.queue=1}]
execute if data storage mgs:multiplayer game{state:"active"} as @a[scores={mgs.lobby.queue=1}] unless score @s mgs.mp.in_game matches 1 run function mgs:v5.4.4/multiplayer/join_game
execute if data storage mgs:multiplayer game{state:"preparing"} as @a[scores={mgs.lobby.queue=1}] unless score @s mgs.mp.in_game matches 1 run function mgs:v5.4.4/multiplayer/join_game

execute if score #lv_mp_round mgs.data matches 1.. unless score #lv_mp_count mgs.data matches 2.. run function mgs:v5.4.4/lobby/multiplayer/cancel_vote
execute unless score #lv_mp_round mgs.data matches 1.. if score #lv_mp_count mgs.data matches 2.. if data storage mgs:multiplayer game{state:"lobby"} run function mgs:v5.4.4/lobby/multiplayer/open_vote
execute if score #lv_mp_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/multiplayer/vote_second
execute unless score #lv_mp_round mgs.data matches 1.. unless score #lv_mp_count mgs.data matches 2.. if data storage mgs:multiplayer game{state:"lobby"} run title @a[scores={mgs.lobby.queue=1}] actionbar [{"translate":"mgs.waiting_for_players","fallback":"Waiting for players: ","color":"aqua"},{"score":{"name":"#lv_mp_count","objective":"mgs.data"},"color":"yellow"},{"text":"/2","color":"yellow"}]

# A game nobody is online in waits 10 minutes for them, then frees the mode.
execute unless entity @a[scores={mgs.mp.in_game=1}] unless data storage mgs:multiplayer game{state:"lobby"} run scoreboard players add #lv_mp_empty mgs.data 1
execute if entity @a[scores={mgs.mp.in_game=1}] run scoreboard players set #lv_mp_empty mgs.data 0
execute if data storage mgs:multiplayer game{state:"lobby"} run scoreboard players set #lv_mp_empty mgs.data 0
execute if score #lv_mp_empty mgs.data matches 600.. run function mgs:v5.4.4/multiplayer/stop

