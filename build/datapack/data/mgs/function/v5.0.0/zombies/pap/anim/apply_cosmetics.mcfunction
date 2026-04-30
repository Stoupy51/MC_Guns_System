
#> mgs:v5.0.0/zombies/pap/anim/apply_cosmetics
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/step
#

execute store result storage mgs:temp _pap_cosm_fetch.id int 1 run scoreboard players get @s mgs.zb.pap.id
function mgs:v5.0.0/zombies/pap/anim/fetch_cosmetics with storage mgs:temp _pap_cosm_fetch
execute as @n[tag=mgs.pap_weapon_display,distance=..2] run function mgs:v5.0.0/zombies/pap/anim/apply_cosmetics_to_display

