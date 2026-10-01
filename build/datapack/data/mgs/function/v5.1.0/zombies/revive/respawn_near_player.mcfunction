
#> mgs:v5.1.0/zombies/revive/respawn_near_player
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/revive_complete
#			mgs:v5.1.0/zombies/revive/do_round_respawn
#			mgs:v5.1.0/zombies/revive/void_revive_whos_who
#			mgs:v5.1.0/zombies/revive/void_revive_solo_qr
#

tag @s add mgs.spawn_pending
# #has_candidate stays 0 without an alive teammate: the `as @r` body never runs, so `store success` never writes.
scoreboard players set #has_candidate mgs.data 0
execute as @r[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,limit=1] at @s store success score #has_candidate mgs.data run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate
# No alive teammate: the spawn nearest @s.
execute if score #has_candidate mgs.data matches 0 run tag @n[tag=mgs.spawn_point,tag=mgs.spawn_zb_player,tag=mgs.spawn_unlocked] add mgs.spawn_candidate
execute as @n[tag=mgs.spawn_candidate] run function mgs:v5.1.0/shared/tp_to_spawn {mode:"zombies"}
tag @e[tag=mgs.spawn_candidate] remove mgs.spawn_candidate
tag @a[tag=mgs.spawn_pending] remove mgs.spawn_pending

