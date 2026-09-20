
#> mgs:v5.1.0/zombies/pap/anim/trigger_coming_out
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/anim/step
#

# Slide weapon horizontally out to the left over 30 ticks (no rotation/size changes)
execute as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^0.6
playsound mgs:zombies/pap/dispense ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

