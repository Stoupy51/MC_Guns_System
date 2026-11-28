
#> mgs:v5.4.4/lobby/missions/launch
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/missions/resolve
#

scoreboard players set #lv_mi_round mgs.data 0
data modify storage mgs:missions game.map_id set from storage mgs:lobby missions.winner.map_id

scoreboard players set @a[scores={mgs.lobby.queue=3}] mgs.mi.in_game 1
execute as @r[scores={mgs.lobby.queue=3}] run function mgs:v5.4.4/missions/start

# A refused start told its player why; the queue votes again.
execute if data storage mgs:missions game{state:"lobby"} run scoreboard players set @a[scores={mgs.lobby.queue=3}] mgs.mi.in_game 0

