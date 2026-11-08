
#> mgs:v5.4.1/zombies/xp/pay_spend
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/xp/spend_delta
#

scoreboard players operation #xp_spent mgs.data = #xp_gain mgs.data
scoreboard players operation #xp_spent mgs.data *= #100 mgs.data
scoreboard players operation @s mgs.zb.xp_spent_acc -= #xp_spent mgs.data

# No message: spending is a trickle with its own feedback.
function mgs:v5.4.1/progression/zb/award_points_spent

