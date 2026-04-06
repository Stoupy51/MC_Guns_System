
#> mgs:v5.0.0/zombies/pap/anim/trigger_retreat
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/step
#

# Weapon glows while collectible, start retreat: slide back to center over 119 ticks (no rotation/size changes)
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {teleport_duration:20,Glowing:true}

# Sound + particle burst
particle end_rod ~ ~1.0 ~ 0.5 0.3 0.5 0.1 20 force
playsound minecraft:entity.player.levelup ambient @a[distance=..30] ~ ~ ~ 0.8 1.0
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.weapon_upgraded_collect_it_before_it_retreats","color":"aqua"}]

