
#> mgs:v5.1.0/multiplayer/summon_spawn_iter
#
# @executed	"","\ud83c\udfc6 ",{"translate":"mgs.score_limit"}],"tooltip":{"translate":"mgs.set_the_score_needed_to_win"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}},{"label":["","\u23f1 ",{"translate":"mgs.time_limit"}],"tooltip":{"translate":"mgs.set_the_match_time_limit"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}},{"label":["","\ud83d\uddfa ",{"translate":"mgs.select_map","color":"aqua"}],"tooltip":{"translate":"mgs.browse_and_select_a_map"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/map_select"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_game"}},{"label":{"translate":"mgs.red_team","color":"red"},"tooltip":{"translate":"mgs.join_red_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_red"}},{"label":{"translate":"mgs.blue_team","color":"blue"},"tooltip":{"translate":"mgs.join_blue_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_blue"}},{"label":{"translate":"mgs.auto_team","color":"yellow"},"tooltip":{"translate":"mgs.auto_balance_across_red_blue_in_ffa_seats_everyone_on_the_single"},"action":{"type":"run_command","command":"/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.assign_players_to_red_blue_teams"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_multiplayer"}}],"columns":2,"exit_action":{"label":["","\u25c0 ",{"translate":"mgs.back","color":"gray"}
#
# @within	mgs:v5.1.0/multiplayer/summon_spawns
#			mgs:v5.1.0/multiplayer/summon_spawn_iter
#

# Read relative coords
execute store result score #sx mgs.data run data get storage mgs:temp _spawn_iter[0][0]
execute store result score #sy mgs.data run data get storage mgs:temp _spawn_iter[0][1]
execute store result score #sz mgs.data run data get storage mgs:temp _spawn_iter[0][2]
execute store result score #syaw mgs.data run data get storage mgs:temp _spawn_iter[0][3] 100

# Convert to absolute
scoreboard players operation #sx mgs.data += #gm_base_x mgs.data
scoreboard players operation #sy mgs.data += #gm_base_y mgs.data
scoreboard players operation #sz mgs.data += #gm_base_z mgs.data

# Store position + yaw for macro
execute store result storage mgs:temp _spos.x double 1 run scoreboard players get #sx mgs.data
execute store result storage mgs:temp _spos.y double 1 run scoreboard players get #sy mgs.data
execute store result storage mgs:temp _spos.z double 1 run scoreboard players get #sz mgs.data
execute store result storage mgs:temp _spos.yaw double 0.01 run scoreboard players get #syaw mgs.data
data modify storage mgs:temp _spos.tag set from storage mgs:temp _spawn_tag

# Summon
function mgs:v5.1.0/multiplayer/summon_spawn_at with storage mgs:temp _spos

# Next
data remove storage mgs:temp _spawn_iter[0]
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.1.0/multiplayer/summon_spawn_iter

