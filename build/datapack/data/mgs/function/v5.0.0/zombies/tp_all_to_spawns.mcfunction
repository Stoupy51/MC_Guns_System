
#> mgs:v5.0.0/zombies/tp_all_to_spawns
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

execute as @a[scores={mgs.zb.in_game=1}] at @s run function mgs:v5.0.0/zombies/pick_spawn
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used

