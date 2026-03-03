
#> mgs:v5.0.0/multiplayer/custom/fav_pd_rebuild
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/toggle_favorite
#			mgs:v5.0.0/multiplayer/custom/fav_pd_rebuild
#

# Check if this entry's PID matches ours
execute store result score #pd_pid mgs.data run data get storage mgs:temp _pd_src[0].pid
execute if score #pd_pid mgs.data = @s mgs.mp.pid run function mgs:v5.0.0/multiplayer/custom/fav_modify_entry

# Append entry (possibly modified) to player_data
data modify storage mgs:multiplayer player_data append from storage mgs:temp _pd_src[0]

# Next
data remove storage mgs:temp _pd_src[0]
execute if data storage mgs:temp _pd_src[0] run function mgs:v5.0.0/multiplayer/custom/fav_pd_rebuild

