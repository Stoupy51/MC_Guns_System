
#> mgs:v5.1.0/zombies/revive/hide_body
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/revive_complete
#			mgs:v5.1.0/zombies/whos_who/forfeit
#			mgs:v5.1.0/zombies/revive/revive_complete
#			mgs:v5.1.0/zombies/revive/bleed_out
#

tag @e[tag=mgs.downed_mannequin,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] add mgs.downed_mine_temp
tp @n[tag=mgs.downed_mine_temp] ~ -10000 ~
execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tp @s ~ -10000 ~
tag @n[tag=mgs.downed_mine_temp] remove mgs.downed_mannequin
execute as @e[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run tag @s remove mgs.downed_hud
tag @e[tag=mgs.downed_mine_temp] remove mgs.downed_mine_temp
execute as @e[tag=mgs.downed_cam,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] run kill @s

