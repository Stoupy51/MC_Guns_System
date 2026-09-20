
#> mgs:v5.1.0/zombies/pap/anim/trigger_retreat
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/anim/step
#

# Weapon glows while collectible, start retreat: slide back to center over 119 ticks (no rotation/size changes)
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {Glowing:true}

# Retreat runs at the normal 1x rate even for Timeslip machines (only the upgrade is sped up), and
# its slides are 20 real ticks apart — restore the full 20-tick interpolation so the retreat glides
# smoothly (anim/start shortens it to 7 for the sped-up upgrade slides on Timeslip machines)
data modify entity @n[tag=mgs.pap_weapon_display,distance=..2] teleport_duration set value 20

# Sound + particle burst
execute positioned ~ ~-2 ~ run particle end_rod ~ ~1.0 ~ 0.5 0.3 0.5 0.1 20 force @a[distance=..48]
playsound mgs:zombies/pap/ready ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.weapon_upgraded_collect_it_before_it_retreats","color":"aqua"}]

