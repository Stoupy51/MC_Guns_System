
#> mgs:v5.1.0/zombies/whos_who/despawn_body
#
# @executed	as @a[tag=mgs.ww_active,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/whos_who/revive_complete
#			mgs:v5.1.0/zombies/whos_who/bleed_out
#

scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
kill @e[tag=mgs.ww_body,predicate=mgs:v5.1.0/zombies/revive/downed_id_match]
kill @e[tag=mgs.ww_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match]

