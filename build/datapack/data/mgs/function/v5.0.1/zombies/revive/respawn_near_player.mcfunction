
#> mgs:v5.0.1/zombies/revive/respawn_near_player
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.0.1/zombies/revive/do_round_respawn
#

tag @s add mgs.spawn_pending
# #has_candidate stays 0 if there is no alive teammate (the `as @r` body never runs, so its
# `store success` never writes); the success flag then replaces a global @e existence scan.
scoreboard players set #has_candidate mgs.data 0
execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] at @s store success score #has_candidate mgs.data run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate
# Fallback: if no alive teammate, use the unlocked player spawn nearest to @s
execute if score #has_candidate mgs.data matches 0 run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate
execute as @n[tag=mgs.spawn_candidate] run function mgs:v5.0.1/zombies/tp_to_spawn
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending

