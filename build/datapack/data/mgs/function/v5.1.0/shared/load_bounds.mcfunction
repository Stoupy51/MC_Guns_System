
#> mgs:v5.1.0/shared/load_bounds
#
# @executed	"","\ud83e\uddec ",{"translate":"mgs.variant"}],"tooltip":{"translate":"mgs.choose_the_zombies_experience"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/zombies/setup/variant"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/stop"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.add_or_remove_players_from_the_zombies_game"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_zombies"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.all_players_join","color":"green"}],"tooltip":{"translate":"mgs.add_every_online_player_to_the_zombies_game"},"action":{"type":"run_command","command":"/execute as @a run function mgs:v5.1.0/players/zb_join"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_zombies_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/zombies/join_game"}}
#
# @within	mgs:v5.1.0/zombies/start {mode:"zombies"}
#			mgs:v5.1.0/multiplayer/start {mode:"multiplayer"}
#			mgs:v5.1.0/missions/start {mode:"missions"}
#
# @args		mode (string)
#

$execute store result score #bound_x1 mgs.data run data get storage mgs:$(mode) game.map.boundaries[0][0]
$execute store result score #bound_y1 mgs.data run data get storage mgs:$(mode) game.map.boundaries[0][1]
$execute store result score #bound_z1 mgs.data run data get storage mgs:$(mode) game.map.boundaries[0][2]
$execute store result score #bound_x2 mgs.data run data get storage mgs:$(mode) game.map.boundaries[1][0]
$execute store result score #bound_y2 mgs.data run data get storage mgs:$(mode) game.map.boundaries[1][1]
$execute store result score #bound_z2 mgs.data run data get storage mgs:$(mode) game.map.boundaries[1][2]
scoreboard players operation #bound_x1 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y1 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z1 mgs.data += #gm_base_z mgs.data
scoreboard players operation #bound_x2 mgs.data += #gm_base_x mgs.data
scoreboard players operation #bound_y2 mgs.data += #gm_base_y mgs.data
scoreboard players operation #bound_z2 mgs.data += #gm_base_z mgs.data
function mgs:v5.1.0/shared/normalize_bounds

