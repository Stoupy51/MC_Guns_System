
#> mgs:v5.4.2/multiplayer/kill_cam/drive_puppet
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/play_sample
#

execute as @e[type=minecraft:mannequin,tag=mgs.kc_puppet,predicate=mgs:v5.4.2/multiplayer/kill_cam/id_match] at 006d6773-0000-0000-0000-000000006b63 run return run function mgs:v5.4.2/multiplayer/kill_cam/move_puppet
execute at 006d6773-0000-0000-0000-000000006b63 summon minecraft:mannequin run function mgs:v5.4.2/multiplayer/kill_cam/init_puppet

