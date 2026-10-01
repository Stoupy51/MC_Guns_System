
#> mgs:v5.1.0/zombies/pap/anim/trigger_retreat
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/anim/step
#

data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {Glowing:true}

# The retreat runs at 1x even on Timeslip machines and its slides are 20 ticks apart, so the
# 20-tick interpolation that anim/start shortened comes back.
data modify entity @n[tag=mgs.pap_weapon_display,distance=..2] teleport_duration set value 20

execute positioned ~ ~-2 ~ run particle end_rod ~ ~1.0 ~ 0.5 0.3 0.5 0.1 20 force @a[distance=..48]
playsound mgs:zombies/pap/ready ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.weapon_upgraded_collect_it_before_it_retreats","color":"aqua"}]

