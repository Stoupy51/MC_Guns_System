
#> mgs:v5.4.2/multiplayer/kill_cam/drop_frames_without_killer
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/start with storage mgs:temp _kc
#			mgs:v5.4.2/multiplayer/kill_cam/drop_frames_without_killer with storage mgs:temp _kc
#
# @args		killer (unknown)
#

$execute if data storage mgs:kill_cam frames[0].s[{id:$(killer)}] run return 0
data remove storage mgs:kill_cam frames[0]
execute if data storage mgs:kill_cam frames[0] run function mgs:v5.4.2/multiplayer/kill_cam/drop_frames_without_killer with storage mgs:temp _kc

