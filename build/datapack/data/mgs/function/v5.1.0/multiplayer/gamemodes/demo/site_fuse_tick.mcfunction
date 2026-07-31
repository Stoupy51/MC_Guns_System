
#> mgs:v5.1.0/multiplayer/gamemodes/demo/site_fuse_tick
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/tick [ as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s ]
#

scoreboard players operation @s mgs.demo_fuse -= #tick_delta mgs.data
execute if score @s mgs.demo_fuse matches ..0 run function mgs:v5.1.0/multiplayer/gamemodes/demo/site_destroyed

