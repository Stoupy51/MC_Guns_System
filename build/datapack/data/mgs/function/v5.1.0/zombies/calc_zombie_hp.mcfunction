
#> mgs:v5.1.0/zombies/calc_zombie_hp
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/types/normal
#			mgs:v5.1.0/zombies/types/dog
#

execute if score #zb_round mgs.data matches ..9 run scoreboard players operation #zb_hp mgs.data = #zb_round mgs.data
execute if score #zb_round mgs.data matches ..9 run scoreboard players operation #zb_hp mgs.data *= #100 mgs.data
execute if score #zb_round mgs.data matches ..9 run scoreboard players add #zb_hp mgs.data 50

execute if score #zb_round mgs.data matches 10.. run scoreboard players operation #zb_exp_round mgs.data = #zb_round mgs.data
execute if score #zb_round mgs.data matches 10.. run scoreboard players remove #zb_exp_round mgs.data 9

execute if score #zb_round mgs.data matches 10.. run data modify storage bs:in math.pow.x set value 1.1f
execute if score #zb_round mgs.data matches 10.. store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round mgs.data
execute if score #zb_round mgs.data matches 10.. run function #bs.math:pow
execute if score #zb_round mgs.data matches 10.. store result score #zb_hp mgs.data run data get storage bs:out math.pow 950

scoreboard players operation #zb_hp mgs.data *= #2 mgs.data
scoreboard players operation #zb_hp mgs.data /= #15 mgs.data

# Also catches int overflow on very high rounds.
execute unless score #zb_hp mgs.data matches 15..2048 run scoreboard players set #zb_hp mgs.data 2048

