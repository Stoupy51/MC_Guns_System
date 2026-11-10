
#> mgs:v5.4.1/multiplayer/kill_cam/cleanup
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/stop
#

execute as @a[tag=mgs.kc_viewer] run function mgs:v5.4.1/multiplayer/kill_cam/return_home
tag @a remove mgs.kc_viewer
tag @a remove mgs.kc_killer
execute as @e[type=minecraft:mannequin,tag=mgs.kc_puppet] at @s run function mgs:v5.4.1/multiplayer/kill_cam/vanish
kill @e[tag=mgs.kill_cam]
function mgs:v5.4.1/multiplayer/kill_cam/close
scoreboard players set #kc_final mgs.data 0
data remove storage mgs:kill_cam frame

