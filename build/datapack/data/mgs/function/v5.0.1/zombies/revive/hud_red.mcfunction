
#> mgs:v5.0.1/zombies/revive/hud_red
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/revive/downed_tick
#

data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.0.1/zombies/revive/downed_id_match] text[0] set value {"selector":"@a[tag=mgs.downed_spectator,sort=nearest,limit=1]","color":"red"}
data modify entity @n[tag=mgs.downed_hud,predicate=mgs:v5.0.1/zombies/revive/downed_id_match] text[1] set value {"text":" ↓","color":"red"}

