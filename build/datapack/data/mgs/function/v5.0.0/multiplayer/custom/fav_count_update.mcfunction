
#> mgs:v5.0.0/multiplayer/custom/fav_count_update
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/toggle_favorite
#

data modify storage mgs:temp _fav_count_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
execute if data storage mgs:temp _fav_count_src[0] run function mgs:v5.0.0/multiplayer/custom/fav_count_rebuild

