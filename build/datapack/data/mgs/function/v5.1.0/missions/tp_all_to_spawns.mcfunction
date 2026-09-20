
#> mgs:v5.1.0/missions/tp_all_to_spawns
#
# @within	mgs:v5.1.0/missions/preload_complete
#

# Teleport every player in this game onto a spawn marker, then free the markers again
execute as @a[scores={mgs.mi.in_game=1}] at @s run function mgs:v5.1.0/missions/pick_spawn
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used

