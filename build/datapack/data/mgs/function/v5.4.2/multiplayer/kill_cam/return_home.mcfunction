
#> mgs:v5.4.2/multiplayer/kill_cam/return_home
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/kill_cam/cleanup [ as @a[tag=mgs.kc_viewer] ]
#

scoreboard players operation #kc_sid mgs.data = @s bs.id
execute at @e[type=minecraft:marker,tag=mgs.kc_home,predicate=mgs:v5.4.2/multiplayer/kill_cam/id_match] run tp @s ~ ~ ~ ~ ~

