
#> mgs:v5.0.0/zombies/pap/anim_trigger_retreat
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_step
#

# Weapon is out — start slow retreat back into machine (60 ticks = 3s). Collectible until inside.
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {Glowing:1b,interpolation_duration:60,start_interpolation:0,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-0.5f,0f],scale:[0.8f,0.8f,0.8f]}}

# Switch to retreat mode (-2 to -62 over 60 ticks)
scoreboard players set @s mgs.pap_anim -2

# Sound + particle burst + broadcast
particle end_rod ~ ~1.2 ~ 0.5 0.5 0.5 0.1 20 force
playsound minecraft:ui.toast.challenge_complete ambient @a[distance=..30] ~ ~ ~ 0.8 1.0
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.weapon_upgraded_collect_it_before_it_goes_back_in","color":"aqua"}]

