
#> mgs:v5.0.0/multiplayer/custom/like_increment_setup
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/like
#

data modify storage mgs:temp _like_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
execute if data storage mgs:temp _like_src[0] run function mgs:v5.0.0/multiplayer/custom/like_increment_rebuild

