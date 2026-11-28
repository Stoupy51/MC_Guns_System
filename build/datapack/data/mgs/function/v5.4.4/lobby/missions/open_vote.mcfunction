
#> mgs:v5.4.4/lobby/missions/open_vote
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/missions/second
#

function mgs:v5.4.4/lobby/vote/collect_maps {mode:"missions",field:"spawning_points.mission"}
function mgs:v5.4.4/lobby/vote/finish_options {mode:"missions"}
execute if score #lv_slots mgs.data matches 0 run return run title @a[scores={mgs.lobby.queue=3}] actionbar {"translate":"mgs.no_missions_map_is_ready_to_play","fallback":"No Missions map is ready to play.","color":"red"}

scoreboard players operation #lv_mi_slots mgs.data = #lv_slots mgs.data
scoreboard players set #lv_mi_round mgs.data 1
scoreboard players set #lv_mi_timer mgs.data 400
function mgs:v5.4.4/lobby/missions/begin_round

