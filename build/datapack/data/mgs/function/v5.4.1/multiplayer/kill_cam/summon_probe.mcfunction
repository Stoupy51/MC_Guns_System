
#> mgs:v5.4.1/multiplayer/kill_cam/summon_probe
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/tick [ at @n[type=minecraft:item_display,tag=mgs.kc_camera] ]
#			mgs:v5.4.1/multiplayer/kill_cam/record [ at @r[scores={mgs.mp.in_game=1},gamemode=!spectator] ]
#			mgs:v5.4.1/multiplayer/kill_cam/start [ at @r[tag=mgs.kc_viewer] ]
#

summon minecraft:marker ~ ~ ~ {UUID:[I;7169907,0,0,27491],Tags:["mgs.kill_cam","mgs.multiplayer_entity"]}

