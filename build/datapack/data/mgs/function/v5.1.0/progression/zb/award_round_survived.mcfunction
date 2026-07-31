
#> mgs:v5.1.0/progression/zb/award_round_survived
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/xp/on_round_end [ as @a[scores={mgs.zb.in_game=1}] ]
#

# ROUND_XP x the round just cleared
scoreboard players operation @s mgs.zb.xp_total += #xp_gain mgs.data
scoreboard players operation @s mgs.zb.xp_prog += #xp_gain mgs.data
function mgs:v5.1.0/progression/zb/settle

