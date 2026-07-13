
#> mgs:v5.0.1/zombies/calc_zombie_hp
#
# @within	mgs:v5.0.1/zombies/types/normal
#

# Exponent: round - 1
scoreboard players operation #zb_exp_round mgs.data = #zb_round mgs.data
scoreboard players remove #zb_exp_round mgs.data 1

# 1.1^(round - 1)
data modify storage bs:in math.pow.x set value 1.1f
execute store result storage bs:in math.pow.y float 1 run scoreboard players get #zb_exp_round mgs.data
function #bs.math:pow

# health = base_health (20) * 1.1^(round - 1)
execute store result score #zb_hp mgs.data run data get storage bs:out math.pow 20

# Cap at Minecraft-safe gameplay max
execute unless score #zb_hp mgs.data matches 15..2048 run scoreboard players set #zb_hp mgs.data 2048

