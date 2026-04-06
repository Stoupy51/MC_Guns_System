
#> mgs:v5.0.0/zombies/pap/anim_trigger_going_in
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_step
#

# Slide weapon from ahead ^0.5 to center over 30 ticks (no rotation/size changes)
execute as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.5
playsound minecraft:block.enchantment_table.use ambient @a[distance=..30] ~ ~ ~ 0.8 1.0

