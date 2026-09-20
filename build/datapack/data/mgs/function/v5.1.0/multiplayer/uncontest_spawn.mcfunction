
#> mgs:v5.1.0/multiplayer/uncontest_spawn
#
# @executed	as @e[tag=mgs.spawn_candidate] & at @s
#
# @within	mgs:v5.1.0/multiplayer/pick_spawn [ as @e[tag=mgs.spawn_candidate] & at @s ]
#

tag @s remove mgs.spawn_candidate
scoreboard players remove #mp_cand_count mgs.data 1

