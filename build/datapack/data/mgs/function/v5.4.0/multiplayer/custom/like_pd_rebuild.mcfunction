
#> mgs:v5.4.0/multiplayer/custom/like_pd_rebuild
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/custom/like
#			mgs:v5.4.0/multiplayer/custom/like_pd_rebuild
#

execute store result score #pd_pid mgs.data run data get storage mgs:temp _pd_src[0].pid
execute if score #pd_pid mgs.data = @s mgs.mp.pid run function mgs:v5.4.0/multiplayer/custom/like_modify_entry

data modify storage mgs:multiplayer player_data append from storage mgs:temp _pd_src[0]

data remove storage mgs:temp _pd_src[0]
execute if data storage mgs:temp _pd_src[0] run function mgs:v5.4.0/multiplayer/custom/like_pd_rebuild

