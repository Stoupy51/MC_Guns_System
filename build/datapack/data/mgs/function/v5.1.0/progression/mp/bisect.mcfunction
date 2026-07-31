
#> mgs:v5.1.0/progression/mp/bisect
#
# @executed	as @a
#
# @within	mgs:v5.1.0/progression/mp/recompute
#			mgs:v5.1.0/progression/mp/bisect
#

scoreboard players operation #xp_mid mgs.data = #xp_lo mgs.data
scoreboard players operation #xp_mid mgs.data += #xp_hi mgs.data
scoreboard players operation #xp_mid mgs.data /= #2 mgs.data
execute if score #xp_mid mgs.data = #xp_lo mgs.data run return 0

scoreboard players operation #xp_need mgs.data = #xp_mid mgs.data
scoreboard players operation #xp_need mgs.data *= #5 mgs.data
scoreboard players add #xp_need mgs.data 40
scoreboard players operation #xp_lvl_m1 mgs.data = #xp_mid mgs.data
scoreboard players remove #xp_lvl_m1 mgs.data 1
scoreboard players operation #xp_need mgs.data *= #xp_lvl_m1 mgs.data
execute if score @s mgs.mp.xp_total >= #xp_need mgs.data run scoreboard players operation #xp_lo mgs.data = #xp_mid mgs.data
execute if score @s mgs.mp.xp_total < #xp_need mgs.data run scoreboard players operation #xp_hi mgs.data = #xp_mid mgs.data
function mgs:v5.1.0/progression/mp/bisect

