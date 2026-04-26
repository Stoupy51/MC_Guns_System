
#> mgs:v5.0.0/zombies/calc_zombie_hp_exp
#
# @within	mgs:v5.0.0/zombies/calc_zombie_hp
#

scoreboard players operation #zb_exp_round mgs.data = #zb_round mgs.data
scoreboard players remove #zb_exp_round mgs.data 9

data modify storage bs:in math.pow.x set value 1.1f
execute store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round mgs.data
function #bs.math:pow

execute store result score #zb_hp mgs.data run data get storage bs:out math.pow 950
scoreboard players operation #zb_hp mgs.data *= #2 mgs.data
scoreboard players operation #zb_hp mgs.data /= #15 mgs.data

