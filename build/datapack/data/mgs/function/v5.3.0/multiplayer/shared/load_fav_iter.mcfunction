
#> mgs:v5.3.0/multiplayer/shared/load_fav_iter
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/shared/load_player_favorites
#			mgs:v5.3.0/multiplayer/shared/load_fav_iter
#

execute store result score #pd_pid mgs.data run data get storage mgs:temp _pd_iter[0].pid
execute if score #pd_pid mgs.data = @s mgs.mp.pid run data modify storage mgs:temp _cur_favorites set from storage mgs:temp _pd_iter[0].favorites
data remove storage mgs:temp _pd_iter[0]
# Stops once found.
execute unless score #pd_pid mgs.data = @s mgs.mp.pid if data storage mgs:temp _pd_iter[0] run function mgs:v5.3.0/multiplayer/shared/load_fav_iter

