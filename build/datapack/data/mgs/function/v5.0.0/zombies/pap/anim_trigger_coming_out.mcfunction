
#> mgs:v5.0.0/zombies/pap/anim_trigger_coming_out
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_step
#

# Interpolate weapon display upward: Y from -0.5 to +1.2 over 30 ticks, slight scale increase
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {interpolation_duration:30,start_interpolation:0,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,1.2f,0f],scale:[0.85f,0.85f,0.85f]}}
playsound minecraft:block.beacon.activate ambient @a[distance=..30] ~ ~ ~ 1.5 0.8

