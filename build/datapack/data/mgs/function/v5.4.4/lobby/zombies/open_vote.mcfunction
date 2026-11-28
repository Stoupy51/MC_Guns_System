
#> mgs:v5.4.4/lobby/zombies/open_vote
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/zombies/second
#

function mgs:v5.4.4/lobby/vote/collect_maps {mode:"zombies",field:"spawning_points.players"}
function mgs:v5.4.4/lobby/vote/finish_options {mode:"zombies"}
execute if score #lv_slots mgs.data matches 0 run return run title @a[scores={mgs.lobby.queue=2}] actionbar {"translate":"mgs.no_zombies_map_is_ready_to_play","fallback":"No Zombies map is ready to play.","color":"red"}

scoreboard players operation #lv_zb_slots mgs.data = #lv_slots mgs.data
scoreboard players set #lv_zb_round mgs.data 1
scoreboard players set #lv_zb_timer mgs.data 400
function mgs:v5.4.4/lobby/zombies/begin_round

