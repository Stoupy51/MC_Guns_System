
#> mgs:v5.1.0/multiplayer/gamemodes/snd/setup
#
# @executed	"","\ud83c\udfc6 ",{"translate":"mgs.score_limit"}],"tooltip":{"translate":"mgs.set_the_score_needed_to_win"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}},{"label":["","\u23f1 ",{"translate":"mgs.time_limit"}],"tooltip":{"translate":"mgs.set_the_match_time_limit"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}},{"label":["","\ud83d\uddfa ",{"translate":"mgs.select_map","color":"aqua"}],"tooltip":{"translate":"mgs.browse_and_select_a_map"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/map_select"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_game"}},{"label":{"translate":"mgs.red_team","color":"red"},"tooltip":{"translate":"mgs.join_red_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_red"}},{"label":{"translate":"mgs.blue_team","color":"blue"},"tooltip":{"translate":"mgs.join_blue_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_blue"}},{"label":{"translate":"mgs.auto_team","color":"yellow"},"tooltip":{"translate":"mgs.auto_balance_assign"},"action":{"type":"run_command","command":"/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.assign_players_to_red_blue_teams"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_multiplayer"}}
#
# @within	mgs:v5.1.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.search_destroy_attackers_plant_defenders_defuse","color":"yellow"}]

# Store base coordinates for offset
function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Round tracking
scoreboard players set #snd_round mgs.data 1
scoreboard players set #snd_max_rounds mgs.data 6
scoreboard players set #snd_red_wins mgs.data 0
scoreboard players set #snd_blue_wins mgs.data 0

# Red starts as attackers
scoreboard players set #snd_attackers mgs.data 1

# Bomb state: 0=not planted, 2=planted (bomb_timer = explosion countdown)
# Plant/defuse channel progress are tracked separately so the countdown is never clobbered
scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0
scoreboard players set #snd_plant_progress mgs.data 0
scoreboard players set #snd_defuse_progress mgs.data 0

# Round timer (90 seconds = 1800 ticks)
scoreboard players set #snd_round_timer mgs.data 1800

# Summon objective markers (relative → absolute)
data modify storage mgs:temp _snd_iter set from storage mgs:multiplayer game.map.search_and_destroy
execute if data storage mgs:temp _snd_iter[0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/summon_obj

# Start round
function mgs:v5.1.0/multiplayer/gamemodes/snd/start_round

