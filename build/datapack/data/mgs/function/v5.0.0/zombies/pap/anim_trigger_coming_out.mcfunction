
#> mgs:v5.0.0/zombies/pap/anim_trigger_coming_out
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_step
#

# Slide weapon horizontally out to the left with slight elevation over 40 ticks, scale up
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {interpolation_duration:40,start_interpolation:0,transformation:{translation:[-0.8f,0f,0f],scale:[0.6f,0.6f,0.6f]}}
playsound minecraft:block.beacon.activate ambient @a[distance=..30] ~ ~ ~ 1.5 0.8

# Weapon upgraded — notify players
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.weapon_upgraded_collect_it_before_it_retreats","color":"aqua"}]

