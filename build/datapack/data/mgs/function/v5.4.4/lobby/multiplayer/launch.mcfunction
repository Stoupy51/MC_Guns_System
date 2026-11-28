
#> mgs:v5.4.4/lobby/multiplayer/launch
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/resolve
#			mgs:v5.4.4/lobby/multiplayer/map_round
#

scoreboard players set #lv_mp_round mgs.data 0
data modify storage mgs:multiplayer game.gamemode set from storage mgs:lobby multiplayer.preset.gamemode
data modify storage mgs:multiplayer game.score_limit set from storage mgs:lobby multiplayer.preset.score_limit
data modify storage mgs:multiplayer game.time_limit set from storage mgs:lobby multiplayer.preset.time_limit
data modify storage mgs:multiplayer game.map_id set from storage mgs:lobby multiplayer.winner.map_id

scoreboard players set @a[scores={mgs.lobby.queue=1}] mgs.mp.in_game 1
execute as @r[scores={mgs.lobby.queue=1}] run function mgs:v5.4.4/multiplayer/start

# A refused start told its player why; the queue votes again.
execute if data storage mgs:multiplayer game{state:"lobby"} run scoreboard players set @a[scores={mgs.lobby.queue=1}] mgs.mp.in_game 0

