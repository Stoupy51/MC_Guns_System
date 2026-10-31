
#> mgs:v5.3.0/stats/board/refresh_holograms
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/login_as
#			mgs:v5.3.0/stats/zb/game_end
#			mgs:v5.3.0/stats/mp/game_end
#			mgs:v5.3.0/stats/mi/game_end
#			mgs:v5.3.0/stats/admin/reset_board
#

kill @e[type=minecraft:text_display,tag=mgs.lb_text]
tag @e[type=minecraft:marker,tag=mgs.leaderboard] remove mgs.lb_shown

