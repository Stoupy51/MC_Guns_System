
#> mgs:v5.3.0/zombies/xp/earn_delta
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.3.0/zombies/xp/track_points
#

scoreboard players operation @s mgs.st.zb.points_earned += @s mgs.zb.points
scoreboard players operation @s mgs.st.zb.points_earned -= @s mgs.zb.xp_pts_prev

