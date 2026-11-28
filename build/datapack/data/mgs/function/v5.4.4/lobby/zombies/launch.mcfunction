
#> mgs:v5.4.4/lobby/zombies/launch
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/zombies/resolve
#

scoreboard players set #lv_zb_round mgs.data 0
data modify storage mgs:zombies game.map_id set from storage mgs:lobby zombies.winner.map_id

scoreboard players set @a[scores={mgs.lobby.queue=2}] mgs.zb.in_game 1
execute as @r[scores={mgs.lobby.queue=2}] run function mgs:v5.4.4/zombies/start

# A refused start told its player why; the queue votes again.
execute if data storage mgs:zombies game{state:"lobby"} run scoreboard players set @a[scores={mgs.lobby.queue=2}] mgs.zb.in_game 0

