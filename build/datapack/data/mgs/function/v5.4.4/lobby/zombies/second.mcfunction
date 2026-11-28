
#> mgs:v5.4.4/lobby/zombies/second
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/second
#

execute store result score #lv_zb_count mgs.data if entity @a[scores={mgs.lobby.queue=2}]
execute if data storage mgs:zombies game{state:"active"} as @a[scores={mgs.lobby.queue=2}] unless score @s mgs.zb.in_game matches 1 run function mgs:v5.4.4/zombies/join_game

execute if score #lv_zb_round mgs.data matches 1.. unless score #lv_zb_count mgs.data matches 1.. run function mgs:v5.4.4/lobby/zombies/cancel_vote
execute unless score #lv_zb_round mgs.data matches 1.. if score #lv_zb_count mgs.data matches 1.. if data storage mgs:zombies game{state:"lobby"} run function mgs:v5.4.4/lobby/zombies/open_vote
execute if score #lv_zb_round mgs.data matches 1.. run function mgs:v5.4.4/lobby/zombies/vote_second
execute unless score #lv_zb_round mgs.data matches 1.. unless score #lv_zb_count mgs.data matches 1.. if data storage mgs:zombies game{state:"lobby"} run title @a[scores={mgs.lobby.queue=2}] actionbar [{"translate":"mgs.waiting_for_players","fallback":"Waiting for players: ","color":"aqua"},{"score":{"name":"#lv_zb_count","objective":"mgs.data"},"color":"yellow"},{"text":"/1","color":"yellow"}]

# A game nobody is online in waits 10 minutes for them, then frees the mode.
execute unless entity @a[scores={mgs.zb.in_game=1}] unless data storage mgs:zombies game{state:"lobby"} run scoreboard players add #lv_zb_empty mgs.data 1
execute if entity @a[scores={mgs.zb.in_game=1}] run scoreboard players set #lv_zb_empty mgs.data 0
execute if data storage mgs:zombies game{state:"lobby"} run scoreboard players set #lv_zb_empty mgs.data 0
execute if score #lv_zb_empty mgs.data matches 600.. run function mgs:v5.4.4/zombies/stop

