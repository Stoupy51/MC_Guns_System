
#> mgs:v5.1.0/zombies/revive/hud_yellow
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/owner_tick
#			mgs:v5.1.0/zombies/revive/downed_tick
#

data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] text[0].color set value "yellow"
data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] text[1].color set value "yellow"

