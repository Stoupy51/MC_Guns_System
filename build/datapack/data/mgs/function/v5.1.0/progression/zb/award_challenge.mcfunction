
#> mgs:v5.1.0/progression/zb/award_challenge
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/progression/adv/reward_zb
#

# Any challenge unlocked; the tier's payout arrives in #xp_gain
scoreboard players operation @s mgs.zb.xp_total += #xp_gain mgs.data
scoreboard players operation @s mgs.zb.xp_prog += #xp_gain mgs.data
function mgs:v5.1.0/progression/zb/settle

