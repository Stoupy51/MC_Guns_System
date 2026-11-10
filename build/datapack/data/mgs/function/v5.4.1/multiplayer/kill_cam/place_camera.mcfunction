
#> mgs:v5.4.1/multiplayer/kill_cam/place_camera
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/start with storage mgs:temp _kc
#
# @args		killer (unknown)
#

$data modify entity 006d6773-0000-0000-0000-000000006b63 Pos set from storage mgs:kill_cam frames[0].s[{id:$(killer)}].p
$data modify entity 006d6773-0000-0000-0000-000000006b63 Rotation set from storage mgs:kill_cam frames[0].s[{id:$(killer)}].r
execute at 006d6773-0000-0000-0000-000000006b63 run summon minecraft:item_display ~ ~1.62 ~ {teleport_duration:2,Tags:["mgs.kc_camera","mgs.kill_cam","mgs.multiplayer_entity"]}
execute at 006d6773-0000-0000-0000-000000006b63 run tp @n[type=minecraft:item_display,tag=mgs.kc_camera] ~ ~1.62 ~ ~ ~

