
#> mgs:v5.4.1/multiplayer/kill_cam/home_marker
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/add_viewer
#

tag @s add mgs.kc_home
tag @s add mgs.kill_cam
tag @s add mgs.multiplayer_entity
scoreboard players operation @s mgs.mp.kc_id = #kc_sid mgs.data
tp @s ~ ~ ~ ~ ~

