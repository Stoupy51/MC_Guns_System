
#> mgs:v5.0.0/multiplayer/custom/set_default
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# TODO: Set the default custom loadout for auto-selection on game start
tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.default_loadout_coming_soon","color":"yellow"}]

