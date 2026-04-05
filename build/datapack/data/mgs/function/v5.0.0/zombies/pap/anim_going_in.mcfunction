
#> mgs:v5.0.0/zombies/pap/anim_going_in
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_step
#

# Sparse purple dust every 2 ticks
execute store result score #pap_t mgs.data run scoreboard players get @s mgs.pap_anim
scoreboard players operation #pap_t mgs.data %= #2 mgs.data
execute if score #pap_t mgs.data matches 0 run particle dust{color:[0.565,0.0,1.0],scale:1.5} ~ ~1.0 ~ 0.3 0.3 0.3 0 4 force

