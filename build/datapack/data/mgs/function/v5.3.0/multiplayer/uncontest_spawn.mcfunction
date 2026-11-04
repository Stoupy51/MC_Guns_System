
#> mgs:v5.3.0/multiplayer/uncontest_spawn
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/pick_spawn [ as @e[tag=mgs.spawn_candidate] & at @s ]
#

tag @s remove mgs.spawn_candidate
scoreboard players remove #mp_cand_count mgs.data 1

