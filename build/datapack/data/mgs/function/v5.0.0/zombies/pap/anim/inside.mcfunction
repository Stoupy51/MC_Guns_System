
#> mgs:v5.0.0/zombies/pap/anim/inside
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/step
#

# Dense purple dust + end_rod particles every tick
particle dust{color:[0.565,0.0,1.0],scale:1.5} ~ ~0.8 ~ 0.4 0.3 0.4 0 1 force
particle end_rod ~ ~0.8 ~ 0.3 0.2 0.3 0.05 1 force

# Periodic processing sound every 10 ticks
execute store result score #pap_t mgs.data run scoreboard players get @s mgs.pap_anim
scoreboard players operation #pap_t mgs.data %= #10 mgs.data
execute if score #pap_t mgs.data matches 0 run playsound minecraft:block.enchantment_table.use ambient @a[distance=..30] ~ ~ ~ 0.8 1.2

