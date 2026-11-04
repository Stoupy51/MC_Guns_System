
#> mgs:v5.3.0/multiplayer/gamemodes/demo/tally_site
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/gamemodes/demo/pick_sides [ as @e[tag=mgs.demo_obj] & at @s ]
#

execute as @e[tag=mgs.spawn_point,tag=!mgs.spawn_general,limit=1,sort=nearest] run function mgs:v5.3.0/multiplayer/gamemodes/demo/tally_site_spawn

