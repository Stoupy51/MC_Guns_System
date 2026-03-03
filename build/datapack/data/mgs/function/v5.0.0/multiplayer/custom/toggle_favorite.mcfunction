
#> mgs:v5.0.0/multiplayer/custom/toggle_favorite
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1100

# Rebuild player_data, toggling favorite in our entry
data modify storage mgs:temp _pd_src set from storage mgs:multiplayer player_data
data modify storage mgs:multiplayer player_data set value []
scoreboard players set #fav_found mgs.data 0
execute if data storage mgs:temp _pd_src[0] run function mgs:v5.0.0/multiplayer/custom/fav_pd_rebuild

# Notify based on whether it was added or removed
execute if score #fav_found mgs.data matches 1 run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.removed_from_favorites","color":"yellow"}]
execute if score #fav_found mgs.data matches 0 run tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.added_to_favorites","color":"green"}]

# Reopen Marketplace dialog with updated data
function mgs:v5.0.0/multiplayer/marketplace/browse

