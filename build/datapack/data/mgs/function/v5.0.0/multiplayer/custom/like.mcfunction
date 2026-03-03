
#> mgs:v5.0.0/multiplayer/custom/like
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# TODO: Increment loadout's like counter, track in player's liked list
tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.likes_coming_soon","color":"yellow"}]

