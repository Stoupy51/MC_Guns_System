
#> mgs:v5.4.1/multiplayer/kill_cam/trim_deaths
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/trim
#			mgs:v5.4.1/multiplayer/kill_cam/trim_deaths
#			mgs:v5.4.1/multiplayer/kill_cam/start
#

execute store result score #kc_t mgs.data run data get storage mgs:kill_cam deaths[0].t
execute if score #kc_t mgs.data >= #kc_oldest mgs.data run return 0
data remove storage mgs:kill_cam deaths[0]
execute if data storage mgs:kill_cam deaths[0] run function mgs:v5.4.1/multiplayer/kill_cam/trim_deaths

