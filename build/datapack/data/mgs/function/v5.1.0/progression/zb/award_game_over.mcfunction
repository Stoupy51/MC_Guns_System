
#> mgs:v5.1.0/progression/zb/award_game_over
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/xp/on_game_over [ as @a[scores={mgs.zb.in_game=1}] ]
#

# GAME_OVER_XP x the final round
scoreboard players operation @s mgs.zb.xp_total += #xp_gain mgs.data
scoreboard players operation @s mgs.zb.xp_prog += #xp_gain mgs.data
function mgs:v5.1.0/progression/zb/settle

