
#> mgs:v5.4.2/multiplayer/gamemodes/demo/site_fuse_tick
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/gamemodes/demo/tick [ as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s ]
#

scoreboard players operation @s mgs.demo_fuse -= #tick_delta mgs.data
execute if score @s mgs.demo_fuse matches ..0 run function mgs:v5.4.2/multiplayer/gamemodes/demo/site_destroyed

