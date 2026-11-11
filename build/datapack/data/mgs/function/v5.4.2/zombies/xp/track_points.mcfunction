
#> mgs:v5.4.2/zombies/xp/track_points
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/game_tick [ as @a[scores={mgs.zb.in_game=1}] ]
#

execute if score @s mgs.zb.points < @s mgs.zb.xp_pts_prev run function mgs:v5.4.2/zombies/xp/spend_delta
execute if score @s mgs.zb.points > @s mgs.zb.xp_pts_prev run function mgs:v5.4.2/zombies/xp/earn_delta
scoreboard players operation @s mgs.zb.xp_pts_prev = @s mgs.zb.points

