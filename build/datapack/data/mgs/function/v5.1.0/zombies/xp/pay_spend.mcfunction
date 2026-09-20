
#> mgs:v5.1.0/zombies/xp/pay_spend
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/xp/spend_delta
#

scoreboard players operation #xp_spent mgs.data = #xp_gain mgs.data
scoreboard players operation #xp_spent mgs.data *= #100 mgs.data
scoreboard players operation @s mgs.zb.xp_spent_acc -= #xp_spent mgs.data

# No message: spending already had its own feedback, and this is a trickle rather than an event
function mgs:v5.1.0/progression/zb/award_points_spent

