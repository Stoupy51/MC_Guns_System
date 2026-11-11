
#> mgs:v5.4.2/multiplayer/kill_cam/open
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/check_window
#

scoreboard players set #kc_window mgs.data 1
data modify storage mgs:kill_cam frames set value []
data modify storage mgs:kill_cam deaths set value []
data remove storage mgs:kill_cam pending_shots

