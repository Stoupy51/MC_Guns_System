
#> mgs:v5.0.0/multiplayer/custom/toggle_favorite
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# TODO: Add/remove loadout ID from player's favorites list
tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.favorites_coming_soon","color":"yellow"}]

