
#> mgs:v5.4.4/lobby/multiplayer/open_vote
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/second
#

data modify storage mgs:lobby multiplayer.options set value []
execute if score #lv_mp_count mgs.data matches 2.. if data storage mgs:maps multiplayer[].spawning_points.general[0] run data modify storage mgs:lobby multiplayer.options append value {label:{translate:"mgs.free_for_all",fallback:"Free For All",color:"green"},hover:{translate:"mgs.first_to_30_kills_10_minutes",fallback:"First to 30 kills, 10 minutes"},gamemode:"ffa",score_limit:30,time_limit:12000,mode:"multiplayer",field:"spawning_points.general"}
execute if score #lv_mp_count mgs.data matches 2.. if data storage mgs:maps multiplayer[].spawning_points.red[0] run data modify storage mgs:lobby multiplayer.options append value {label:{translate:"mgs.team_deathmatch",fallback:"Team Deathmatch",color:"yellow"},hover:{translate:"mgs.first_team_to_50_kills_10_minutes",fallback:"First team to 50 kills, 10 minutes"},gamemode:"tdm",score_limit:50,time_limit:12000,mode:"multiplayer",field:"spawning_points.red"}
execute if score #lv_mp_count mgs.data matches 4.. if data storage mgs:maps multiplayer[].domination[0] run data modify storage mgs:lobby multiplayer.options append value {label:{translate:"mgs.domination",fallback:"Domination",color:"aqua"},hover:{translate:"mgs.first_team_to_200_points_10_minutes",fallback:"First team to 200 points, 10 minutes"},gamemode:"dom",score_limit:200,time_limit:12000,mode:"multiplayer",field:"domination"}
execute if score #lv_mp_count mgs.data matches 4.. if data storage mgs:maps multiplayer[].hardpoint[0] run data modify storage mgs:lobby multiplayer.options append value {label:{translate:"mgs.hardpoint",fallback:"Hardpoint",color:"dark_purple"},hover:{translate:"mgs.first_team_to_200_points_10_minutes",fallback:"First team to 200 points, 10 minutes"},gamemode:"hp",score_limit:200,time_limit:12000,mode:"multiplayer",field:"hardpoint"}
execute if score #lv_mp_count mgs.data matches 4.. if data storage mgs:maps multiplayer[].search_and_destroy[0] run data modify storage mgs:lobby multiplayer.options append value {label:{translate:"mgs.search_and_destroy",fallback:"Search and Destroy",color:"gold"},hover:{translate:"mgs.first_team_to_4_rounds_no_respawn",fallback:"First team to 4 rounds, no respawn"},gamemode:"snd",score_limit:30,time_limit:12000,mode:"multiplayer",field:"search_and_destroy"}
execute if score #lv_mp_count mgs.data matches 4.. if data storage mgs:maps multiplayer[].search_and_destroy[0] run data modify storage mgs:lobby multiplayer.options append value {label:{translate:"mgs.demolition",fallback:"Demolition",color:"red"},hover:{translate:"mgs.destroy_both_sites_one_attack_per_team",fallback:"Destroy both sites, one attack per team"},gamemode:"demo",score_limit:30,time_limit:12000,mode:"multiplayer",field:"search_and_destroy"}

function mgs:v5.4.4/lobby/vote/finish_options {mode:"multiplayer"}
execute if score #lv_slots mgs.data matches 0 run return run title @a[scores={mgs.lobby.queue=1}] actionbar {"translate":"mgs.no_multiplayer_map_is_ready_to_play","fallback":"No Multiplayer map is ready to play.","color":"red"}

scoreboard players operation #lv_mp_slots mgs.data = #lv_slots mgs.data
scoreboard players set #lv_mp_round mgs.data 1
scoreboard players set #lv_mp_timer mgs.data 400
function mgs:v5.4.4/lobby/multiplayer/begin_round

