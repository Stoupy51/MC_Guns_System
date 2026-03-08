
#> mgs:v5.0.0/zombies/show_points_actionbar
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/game_tick [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] ]
#

title @s actionbar [{"text":"💰 ","color":"gold"},{"score":{"name":"@s","objective":"mgs.zb.points"},"color":"yellow"},{"text":" points","color":"gray"}]

