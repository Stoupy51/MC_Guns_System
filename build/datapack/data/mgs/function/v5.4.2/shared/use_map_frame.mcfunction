
#> mgs:v5.4.2/shared/use_map_frame
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/shared/enter_map {mode:"$(mode)"}
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

