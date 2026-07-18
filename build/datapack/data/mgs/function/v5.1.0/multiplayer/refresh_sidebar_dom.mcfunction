
#> mgs:v5.1.0/multiplayer/refresh_sidebar_dom
#
# @executed	"","\ud83c\udfc6 ",{"translate":"mgs.score_limit"}],"tooltip":{"translate":"mgs.set_the_score_needed_to_win"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}},{"label":["","\u23f1 ",{"translate":"mgs.time_limit"}],"tooltip":{"translate":"mgs.set_the_match_time_limit"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}},{"label":["","\ud83d\uddfa ",{"translate":"mgs.select_map","color":"aqua"}],"tooltip":{"translate":"mgs.browse_and_select_a_map"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/map_select"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_game"}},{"label":{"translate":"mgs.red_team","color":"red"},"tooltip":{"translate":"mgs.join_red_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_red"}},{"label":{"translate":"mgs.blue_team","color":"blue"},"tooltip":{"translate":"mgs.join_blue_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_blue"}},{"label":{"translate":"mgs.auto_team","color":"yellow"},"tooltip":{"translate":"mgs.auto_balance_across_red_blue_in_ffa_seats_everyone_on_the_single"},"action":{"type":"run_command","command":"/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.assign_players_to_red_blue_teams"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_multiplayer"}}
#
# @within	mgs:v5.1.0/multiplayer/create_sidebar_dom
#			mgs:v5.1.0/multiplayer/gamemodes/dom/score_tick
#			mgs:v5.1.0/multiplayer/gamemodes/dom/on_kill
#

# Build point status strings based on ownership scores
# Zone A
execute if score #dom_owner_a mgs.data matches 0 run data modify storage mgs:temp dom_sb.a set value '[" ",{"text":"A: ","color":"gray"},"⚪ ",{"translate":"mgs.neutral","color":"gray"}]'
execute if score #dom_owner_a mgs.data matches 1 run data modify storage mgs:temp dom_sb.a set value '[" ",{"text":"A: ","color":"red"},"🔴 ",{"translate":"mgs.red","color":"red"}]'
execute if score #dom_owner_a mgs.data matches 2 run data modify storage mgs:temp dom_sb.a set value '[" ",{"text":"A: ","color":"blue"},"🔵 ",{"translate":"mgs.blue","color":"blue"}]'

# Zone B
execute if score #dom_owner_b mgs.data matches 0 run data modify storage mgs:temp dom_sb.b set value '[" ",{"text":"B: ","color":"gray"},"⚪ ",{"translate":"mgs.neutral","color":"gray"}]'
execute if score #dom_owner_b mgs.data matches 1 run data modify storage mgs:temp dom_sb.b set value '[" ",{"text":"B: ","color":"red"},"🔴 ",{"translate":"mgs.red","color":"red"}]'
execute if score #dom_owner_b mgs.data matches 2 run data modify storage mgs:temp dom_sb.b set value '[" ",{"text":"B: ","color":"blue"},"🔵 ",{"translate":"mgs.blue","color":"blue"}]'

# Zone C
execute if score #dom_owner_c mgs.data matches 0 run data modify storage mgs:temp dom_sb.c set value '[" ",{"text":"C: ","color":"gray"},"⚪ ",{"translate":"mgs.neutral","color":"gray"}]'
execute if score #dom_owner_c mgs.data matches 1 run data modify storage mgs:temp dom_sb.c set value '[" ",{"text":"C: ","color":"red"},"🔴 ",{"translate":"mgs.red","color":"red"}]'
execute if score #dom_owner_c mgs.data matches 2 run data modify storage mgs:temp dom_sb.c set value '[" ",{"text":"C: ","color":"blue"},"🔵 ",{"translate":"mgs.blue","color":"blue"}]'

# Build sidebar with dynamic point entries
function mgs:v5.1.0/multiplayer/build_sidebar_dom with storage mgs:temp dom_sb

