
#> mgs:v5.1.0/zombies/pap/anim/inside
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/anim/step
#

# Dense purple dust + end_rod particles every tick
execute positioned ~ ~-2 ~ run particle dust{color:[0.565,0.0,1.0],scale:1.5} ~ ~0.8 ~ 0.4 0.3 0.4 0 1 force @a[distance=..48]
execute positioned ~ ~-2 ~ run particle end_rod ~ ~0.8 ~ 0.3 0.2 0.3 0.05 1 force @a[distance=..48]

# Periodic processing sound every 20 ticks
execute store result score #pap_t mgs.data run scoreboard players get @s mgs.pap_anim
scoreboard players operation #pap_t mgs.data %= #20 mgs.data
execute if score #pap_t mgs.data matches 0 run playsound mgs:zombies/pap/pap_loop ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.25 1.0

