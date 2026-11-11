
#> mgs:v5.4.2/multiplayer/kill_cam/drop_early_frames
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/start
#			mgs:v5.4.2/multiplayer/kill_cam/drop_early_frames
#

execute store result score #kc_t mgs.data run data get storage mgs:kill_cam frames[0].t
execute if score #kc_t mgs.data >= #kc_cut mgs.data run return 0
data remove storage mgs:kill_cam frames[0]
execute if data storage mgs:kill_cam frames[0] run function mgs:v5.4.2/multiplayer/kill_cam/drop_early_frames

