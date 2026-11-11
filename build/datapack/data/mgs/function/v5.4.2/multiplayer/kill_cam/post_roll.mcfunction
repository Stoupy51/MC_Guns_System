
#> mgs:v5.4.2/multiplayer/kill_cam/post_roll
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/tick
#

scoreboard players add #kc_now mgs.data 1
execute if score #kc_now mgs.data >= #kc_end_t mgs.data run function mgs:v5.4.2/multiplayer/stop

