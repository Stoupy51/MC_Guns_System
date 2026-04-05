
#> mgs:v5.0.0/zombies/pap/anim_trigger_inside
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_step
#

# Dip down during processing (60 ticks)
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {interpolation_duration:60,start_interpolation:0,transformation:{translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}
playsound minecraft:block.enchantment_table.use ambient @a[distance=..30] ~ ~ ~ 0.8 1.0

