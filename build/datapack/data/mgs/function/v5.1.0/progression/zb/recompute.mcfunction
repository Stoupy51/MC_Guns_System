
#> mgs:v5.1.0/progression/zb/recompute
#
# @executed	as @a
#
# @within	mgs:v5.1.0/progression/zb/init
#			mgs:v5.1.0/progression/recompute_all [ as @a ]
#

execute unless score @s mgs.zb.xp_total matches 0.. run scoreboard players set @s mgs.zb.xp_total 0
execute if score @s mgs.zb.xp_total matches 1000000000.. run scoreboard players set @s mgs.zb.xp_total 1000000000

# Bracket the answer, then halve. Invariant: total_to_reach(#xp_lo) <= xp_total < total_to_reach(#xp_hi).
scoreboard players set #xp_lo mgs.data 1
scoreboard players set #xp_hi mgs.data 16384
function mgs:v5.1.0/progression/zb/bisect

# #xp_lo is the level; whatever the level does not account for is the progress into it
scoreboard players operation @s mgs.zb.xp_level = #xp_lo mgs.data
scoreboard players operation #xp_need mgs.data = #xp_lo mgs.data
scoreboard players operation #xp_need mgs.data *= #5 mgs.data
scoreboard players add #xp_need mgs.data 40
scoreboard players operation #xp_lvl_m1 mgs.data = #xp_lo mgs.data
scoreboard players remove #xp_lvl_m1 mgs.data 1
scoreboard players operation #xp_need mgs.data *= #xp_lvl_m1 mgs.data
scoreboard players operation @s mgs.zb.xp_prog = @s mgs.zb.xp_total
scoreboard players operation @s mgs.zb.xp_prog -= #xp_need mgs.data

function mgs:v5.1.0/progression/zb/refresh_bar

