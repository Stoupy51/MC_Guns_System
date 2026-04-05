
#> mgs:v5.0.0/zombies/pap/anim_timeout
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Weapon not collected — retreat slowly into the machine over 100 ticks
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {Glowing:0b,interpolation_duration:100,start_interpolation:0,transformation:{translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}

# Enter retreat mode: pap_anim -2 → -102 over 100 ticks
scoreboard players set @s mgs.pap_anim -2

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_weapon_was_not_collected_and_is_retreating","color":"red"}]
playsound minecraft:block.fire.extinguish ambient @a[distance=..30] ~ ~ ~ 0.8 0.8

