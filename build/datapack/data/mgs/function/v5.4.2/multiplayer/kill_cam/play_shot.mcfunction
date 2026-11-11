
#> mgs:v5.4.2/multiplayer/kill_cam/play_shot
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/tick
#			mgs:v5.4.2/multiplayer/kill_cam/play_shot
#

execute store result score #kc_sid mgs.data run data get storage mgs:kill_cam frame.shots[0].id
execute if score #kc_sid mgs.data = #kc_killer mgs.data at @n[type=minecraft:item_display,tag=mgs.kc_camera] run particle flash{color:[1.0, 0.8, 0.5, 1.0]} ^-0.35 ^-0.3 ^1 0 0 0 0 1 force @a[tag=mgs.kc_viewer]
execute if data storage mgs:kill_cam frame.shots[0].snd if score #kc_sid mgs.data = #kc_killer mgs.data at @n[type=minecraft:item_display,tag=mgs.kc_camera] run function mgs:v5.4.2/multiplayer/kill_cam/shot_sound with storage mgs:kill_cam frame.shots[0]
execute if data storage mgs:kill_cam frame.shots[0].snd unless score #kc_sid mgs.data = #kc_killer mgs.data at @e[type=minecraft:mannequin,tag=mgs.kc_puppet,predicate=mgs:v5.4.2/multiplayer/kill_cam/id_match] anchored eyes positioned ^ ^ ^ run function mgs:v5.4.2/multiplayer/kill_cam/shot_sound with storage mgs:kill_cam frame.shots[0]
data remove storage mgs:kill_cam frame.shots[0]
execute if data storage mgs:kill_cam frame.shots[0] run function mgs:v5.4.2/multiplayer/kill_cam/play_shot

