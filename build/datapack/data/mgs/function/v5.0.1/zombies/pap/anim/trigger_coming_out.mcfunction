
#> mgs:v5.0.1/zombies/pap/anim/trigger_coming_out
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/pap/anim/step
#

# Slide weapon horizontally out to the left over 30 ticks (no rotation/size changes)
execute as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^0.6
function mgs:v5.0.1/zombies/feedback/sound_pap_dispense

