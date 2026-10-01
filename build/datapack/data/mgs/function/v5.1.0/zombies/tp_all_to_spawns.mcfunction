
#> mgs:v5.1.0/zombies/tp_all_to_spawns
#
# @within	mgs:v5.1.0/zombies/preload_complete
#

# Every player in this game onto a spawn marker, then the markers are freed.
execute as @a[scores={mgs.zb.in_game=1}] at @s run function mgs:v5.1.0/zombies/pick_spawn
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used

