
#> mgs:v5.4.2/zombies/revive/hud_gold
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/whos_who/owner_tick
#			mgs:v5.4.2/zombies/revive/downed_tick
#

data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.4.2/zombies/revive/downed_id_match] text[0].color set value "gold"
data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.4.2/zombies/revive/downed_id_match] text[1].color set value "gold"

