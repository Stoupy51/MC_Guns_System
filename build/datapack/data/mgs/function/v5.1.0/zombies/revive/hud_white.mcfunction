
#> mgs:v5.1.0/zombies/revive/hud_white
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/downed_tick
#

data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] text[0] set value {"selector":"@a[tag=mgs.downed_spectator,sort=nearest,limit=1]","color":"white"}
data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.1.0/zombies/revive/downed_id_match] text[1] set value {"text":" ↓","color":"white"}

