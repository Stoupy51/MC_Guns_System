
#> mgs:v5.0.1/zombies/revive/respawn_near_player
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.0.1/zombies/revive/do_round_respawn
#

tag @s add mgs.spawn_pending
execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] at @s run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate
# Fallback: if no alive teammate, use the unlocked player spawn nearest to @s
execute unless entity @e[tag=mgs.spawn_candidate] run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate
execute as @n[tag=mgs.spawn_candidate] run function mgs:v5.0.1/zombies/tp_to_spawn
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending

