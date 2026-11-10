
#> mgs:v5.4.1/multiplayer/kill_cam/trim
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/record
#

data remove storage mgs:kill_cam frames[0]
execute store result score #kc_oldest mgs.data run data get storage mgs:kill_cam frames[0].t
execute if data storage mgs:kill_cam deaths[0] run function mgs:v5.4.1/multiplayer/kill_cam/trim_deaths

