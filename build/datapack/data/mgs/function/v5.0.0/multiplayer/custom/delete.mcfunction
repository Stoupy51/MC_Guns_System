
#> mgs:v5.0.0/multiplayer/custom/delete
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# TODO: Find and remove loadout from custom_loadouts list if owner matches
tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.delete_coming_soon","color":"yellow"}]

