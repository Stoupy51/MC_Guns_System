
#> mgs:v5.0.0/multiplayer/custom/toggle_favorite
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1100

# TODO: Find player data entry by PID and toggle the loadout ID in favorites[]
tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.favorites_coming_soon","color":"yellow"}]

