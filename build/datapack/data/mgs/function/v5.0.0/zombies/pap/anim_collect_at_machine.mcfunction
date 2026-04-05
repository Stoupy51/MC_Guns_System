
#> mgs:v5.0.0/zombies/pap/anim_collect_at_machine
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_collect [ at @s ]
#

execute store result storage mgs:temp _pap_c.id int 1 run scoreboard players get @s mgs.zb.pap.id
function mgs:v5.0.0/zombies/pap/anim_collect_lookup with storage mgs:temp _pap_c

