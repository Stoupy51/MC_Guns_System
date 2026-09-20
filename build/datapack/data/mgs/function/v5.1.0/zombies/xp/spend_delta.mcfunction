
#> mgs:v5.1.0/zombies/xp/spend_delta
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/xp/track_points
#

scoreboard players operation #xp_spent mgs.data = @s mgs.zb.xp_pts_prev
scoreboard players operation #xp_spent mgs.data -= @s mgs.zb.points
scoreboard players operation @s mgs.zb.xp_spent_acc += #xp_spent mgs.data

# Convert whole chunks and keep the change
scoreboard players operation #xp_gain mgs.data = @s mgs.zb.xp_spent_acc
scoreboard players operation #xp_gain mgs.data /= #100 mgs.data
execute if score #xp_gain mgs.data matches 1.. run function mgs:v5.1.0/zombies/xp/pay_spend

