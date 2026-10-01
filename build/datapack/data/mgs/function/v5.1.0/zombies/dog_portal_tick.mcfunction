
#> mgs:v5.1.0/zombies/dog_portal_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

# Phase 1 (30 ticks): a ring on the floor marks the footprint.
particle minecraft:electric_spark ~ ~0.1 ~ 1.1 0.02 1.1 0.0 5 force @a[distance=..48]

# Phase 2 (last 20): the charge climbs out of the floor.
execute if score @s mgs.zb.rise_tick matches ..20 run particle minecraft:electric_spark ~ ~0.7 ~ 0.35 0.9 0.35 0.03 8 force @a[distance=..48]

# Phase 3 (last 10): a column forms and the ring tightens.
execute if score @s mgs.zb.rise_tick matches ..10 run particle minecraft:end_rod ~ ~1.2 ~ 0.12 1.3 0.12 0.01 5 force @a[distance=..48]
execute if score @s mgs.zb.rise_tick matches ..10 run particle minecraft:crit ~ ~0.2 ~ 0.45 0.08 0.45 0.06 8 force @a[distance=..32]

# Crackle every 5 ticks, with the same volume rule as the strike.
scoreboard players operation #zb_portal_mod mgs.data = @s mgs.zb.rise_tick
scoreboard players operation #zb_portal_mod mgs.data %= #5 mgs.data
execute if score #zb_portal_mod mgs.data matches 0 run playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..32] ~ ~ ~ 2.0 0.6 0.3

scoreboard players remove @s mgs.zb.rise_tick 1
execute if score @s mgs.zb.rise_tick matches ..0 run function mgs:v5.1.0/zombies/dog_portal_strike

