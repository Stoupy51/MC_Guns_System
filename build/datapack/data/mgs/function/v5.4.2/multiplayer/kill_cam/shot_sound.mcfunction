
#> mgs:v5.4.2/multiplayer/kill_cam/shot_sound
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/play_shot with storage mgs:kill_cam frame.shots[0] [ at @n[type=minecraft:item_display,tag=mgs.kc_camera] ]
#			mgs:v5.4.2/multiplayer/kill_cam/play_shot with storage mgs:kill_cam frame.shots[0] [ at @e[type=minecraft:mannequin,tag=mgs.kc_puppet,predicate=mgs:v5.4.2/multiplayer/kill_cam/id_match] & anchored eyes & positioned ^ ^ ^ ]
#
# @args		snd (unknown)
#

$playsound mgs:$(snd) player @a[tag=mgs.kc_viewer] ~ ~ ~ 0.35 1 0.10

