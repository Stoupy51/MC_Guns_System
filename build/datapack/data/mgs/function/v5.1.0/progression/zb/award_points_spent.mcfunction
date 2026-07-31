
#> mgs:v5.1.0/progression/zb/award_points_spent
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/xp/pay_spend
#

# One XP per POINTS_PER_XP spent, remainder carried
scoreboard players operation @s mgs.zb.xp_total += #xp_gain mgs.data
scoreboard players operation @s mgs.zb.xp_prog += #xp_gain mgs.data
function mgs:v5.1.0/progression/zb/settle

