
#> mgs:v5.4.2/multiplayer/kill_cam/play_sample
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/tick
#			mgs:v5.4.2/multiplayer/kill_cam/play_sample
#

execute store result score #kc_sid mgs.data run data get storage mgs:kill_cam frame.s[0].id
data modify entity 006d6773-0000-0000-0000-000000006b63 Pos set from storage mgs:kill_cam frame.s[0].p
data modify entity 006d6773-0000-0000-0000-000000006b63 Rotation set from storage mgs:kill_cam frame.s[0].r
execute store success score #kc_sneak mgs.data if data storage mgs:kill_cam frame.s[0].sneak

execute if score #kc_sid mgs.data = #kc_killer mgs.data if score #kc_sneak mgs.data matches 0 at 006d6773-0000-0000-0000-000000006b63 run tp @n[type=minecraft:item_display,tag=mgs.kc_camera] ~ ~1.62 ~ ~ ~
execute if score #kc_sid mgs.data = #kc_killer mgs.data if score #kc_sneak mgs.data matches 1 at 006d6773-0000-0000-0000-000000006b63 run tp @n[type=minecraft:item_display,tag=mgs.kc_camera] ~ ~1.27 ~ ~ ~
execute unless score #kc_sid mgs.data = #kc_killer mgs.data run function mgs:v5.4.2/multiplayer/kill_cam/drive_puppet

data remove storage mgs:kill_cam frame.s[0]
execute if data storage mgs:kill_cam frame.s[0] run function mgs:v5.4.2/multiplayer/kill_cam/play_sample

