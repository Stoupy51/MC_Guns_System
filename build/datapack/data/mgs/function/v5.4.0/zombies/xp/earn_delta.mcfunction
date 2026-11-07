
#> mgs:v5.4.0/zombies/xp/earn_delta
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/xp/track_points
#

scoreboard players operation @s mgs.st.zb.points_earned += @s mgs.zb.points
scoreboard players operation @s mgs.st.zb.points_earned -= @s mgs.zb.xp_pts_prev

