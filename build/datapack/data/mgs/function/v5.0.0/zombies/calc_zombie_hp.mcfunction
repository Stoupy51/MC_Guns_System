
#> mgs:v5.0.0/zombies/calc_zombie_hp
#
# @within	mgs:v5.0.0/zombies/types/normal
#

# R1-9: linear growth
execute if score #zb_round mgs.data matches ..9 run function mgs:v5.0.0/zombies/calc_zombie_hp_linear

# R10+: exponential growth
execute if score #zb_round mgs.data matches 10.. run function mgs:v5.0.0/zombies/calc_zombie_hp_exp

# Cap at Minecraft-safe gameplay max
execute unless score #zb_hp mgs.data matches 15..2048 run scoreboard players set #zb_hp mgs.data 2048

