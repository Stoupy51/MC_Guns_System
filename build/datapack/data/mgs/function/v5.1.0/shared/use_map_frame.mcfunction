
#> mgs:v5.1.0/shared/use_map_frame
#
# @within	mgs:v5.1.0/zombies/game_tick {mode:"zombies"}
#			mgs:v5.1.0/zombies/preload_complete {mode:"zombies"}
#			mgs:v5.1.0/zombies/stop {mode:"zombies"}
#			mgs:v5.1.0/multiplayer/game_tick {mode:"multiplayer"}
#			mgs:v5.1.0/multiplayer/stop {mode:"multiplayer"}
#			mgs:v5.1.0/missions/game_tick {mode:"missions"}
#			mgs:v5.1.0/missions/preload_complete {mode:"missions"}
#			mgs:v5.1.0/missions/stop {mode:"missions"}
#
# @args		mode (string)
#

$scoreboard players operation #gm_base_x mgs.data = #$(mode)_base_x mgs.data
$scoreboard players operation #gm_base_y mgs.data = #$(mode)_base_y mgs.data
$scoreboard players operation #gm_base_z mgs.data = #$(mode)_base_z mgs.data
$scoreboard players operation #bound_x1 mgs.data = #$(mode)_bound_x1 mgs.data
$scoreboard players operation #bound_y1 mgs.data = #$(mode)_bound_y1 mgs.data
$scoreboard players operation #bound_z1 mgs.data = #$(mode)_bound_z1 mgs.data
$scoreboard players operation #bound_x2 mgs.data = #$(mode)_bound_x2 mgs.data
$scoreboard players operation #bound_y2 mgs.data = #$(mode)_bound_y2 mgs.data
$scoreboard players operation #bound_z2 mgs.data = #$(mode)_bound_z2 mgs.data

