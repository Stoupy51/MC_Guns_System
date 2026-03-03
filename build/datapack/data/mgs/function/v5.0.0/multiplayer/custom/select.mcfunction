
#> mgs:v5.0.0/multiplayer/custom/select
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# TODO: Look up custom loadout by ID and apply it (similar to apply_class)
tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.custom_loadout_selection_coming_soon","color":"yellow"}]

