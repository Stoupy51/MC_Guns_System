
#> mgs:v5.4.4/lobby/multiplayer/map_round
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/resolve
#

data modify storage mgs:lobby multiplayer.preset set from storage mgs:lobby multiplayer.winner
function mgs:v5.4.4/lobby/vote/collect_maps with storage mgs:lobby multiplayer.preset
function mgs:v5.4.4/lobby/vote/finish_options {mode:"multiplayer"}
scoreboard players operation #lv_mp_slots mgs.data = #lv_slots mgs.data

# A single map needs no second vote.
execute if score #lv_mp_slots mgs.data matches 1 run data modify storage mgs:lobby multiplayer.winner set from storage mgs:lobby multiplayer.options[0]
execute if score #lv_mp_slots mgs.data matches 1 run return run function mgs:v5.4.4/lobby/multiplayer/launch

scoreboard players set #lv_mp_round mgs.data 2
scoreboard players set #lv_mp_timer mgs.data 200
function mgs:v5.4.4/lobby/multiplayer/begin_round

