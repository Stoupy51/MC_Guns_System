
#> mgs:v5.1.0/zombies/calc_zombie_hp
#
# @within	mgs:v5.1.0/zombies/types/normal
#			mgs:v5.1.0/zombies/types/dog
#

# Rounds 1-9: bo_hp = 50 + 100 * round
execute if score #zb_round mgs.data matches ..9 run scoreboard players operation #zb_hp mgs.data = #zb_round mgs.data
execute if score #zb_round mgs.data matches ..9 run scoreboard players operation #zb_hp mgs.data *= #100 mgs.data
execute if score #zb_round mgs.data matches ..9 run scoreboard players add #zb_hp mgs.data 50

# Round 10+: exponent = round - 9
execute if score #zb_round mgs.data matches 10.. run scoreboard players operation #zb_exp_round mgs.data = #zb_round mgs.data
execute if score #zb_round mgs.data matches 10.. run scoreboard players remove #zb_exp_round mgs.data 9

# Round 10+: bo_hp = 950 * 1.1^(round - 9)
execute if score #zb_round mgs.data matches 10.. run data modify storage bs:in math.pow.x set value 1.1f
execute if score #zb_round mgs.data matches 10.. store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round mgs.data
execute if score #zb_round mgs.data matches 10.. run function #bs.math:pow
execute if score #zb_round mgs.data matches 10.. store result score #zb_hp mgs.data run data get storage bs:out math.pow 950

# Convert BO HP to Minecraft scale: hp = bo_hp * 2 / 15 (R1: 150 -> 20 HP)
scoreboard players operation #zb_hp mgs.data *= #2 mgs.data
scoreboard players operation #zb_hp mgs.data /= #15 mgs.data

# Cap at Minecraft-safe gameplay max (also catches int overflow on very high rounds)
execute unless score #zb_hp mgs.data matches 15..2048 run scoreboard players set #zb_hp mgs.data 2048

