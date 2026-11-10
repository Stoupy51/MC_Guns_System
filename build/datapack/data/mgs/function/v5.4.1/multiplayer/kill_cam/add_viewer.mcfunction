
#> mgs:v5.4.1/multiplayer/kill_cam/add_viewer
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/start [ as @a[tag=mgs.kc_viewer] & at @s ]
#

scoreboard players operation #kc_sid mgs.data = @s bs.id
execute summon minecraft:marker run function mgs:v5.4.1/multiplayer/kill_cam/home_marker
gamemode spectator @s
spectate @n[type=minecraft:item_display,tag=mgs.kc_camera] @s

