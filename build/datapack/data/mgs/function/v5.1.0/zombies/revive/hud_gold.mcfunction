
#> mgs:v5.1.0/zombies/revive/hud_gold
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick
#

data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] text[0].color set value "gold"
data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] text[1].color set value "gold"

