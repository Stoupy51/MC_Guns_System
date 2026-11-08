
#> mgs:v5.4.1/missions/tp_all_to_spawns
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/missions/preload_complete
#

# Every player in this game onto a spawn marker, then the markers are freed.
execute as @a[scores={mgs.mi.in_game=1}] at @s run function mgs:v5.4.1/missions/pick_spawn
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used

