
#> mgs:v5.0.0/zombies/pap/anim_trigger_retreat
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_step
#

# Weapon glows while collectible, start retreat: slide back to center and down over 100 ticks
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {Glowing:1b,interpolation_duration:100,start_interpolation:0,transformation:{translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}

# Switch to retreat mode (-2 to -102 over 100 ticks)
scoreboard players set @s mgs.pap_anim -2

# Sound + particle burst
particle end_rod ~ ~1.0 ~ 0.5 0.3 0.5 0.1 20 force
playsound minecraft:entity.player.levelup ambient @a[distance=..30] ~ ~ ~ 0.8 1.0
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_weapon_is_retreating_collect_it_now","color":"yellow"}]

