
#> mgs:v5.0.0/multiplayer/custom/like
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1200

# TODO: Find loadout by ID, increment likes counter, add to player's liked[] list
tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.likes_coming_soon","color":"yellow"}]

