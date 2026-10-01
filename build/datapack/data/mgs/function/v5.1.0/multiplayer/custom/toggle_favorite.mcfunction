
#> mgs:v5.1.0/multiplayer/custom/toggle_favorite
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# The trigger value carries the loadout id.
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 20000

# player_data is rebuilt, toggling the favorite in this player's entry.
data modify storage mgs:temp _pd_src set from storage mgs:multiplayer player_data
data modify storage mgs:multiplayer player_data set value []
scoreboard players set #fav_found mgs.data 0
execute if data storage mgs:temp _pd_src[0] run function mgs:v5.1.0/multiplayer/custom/fav_pd_rebuild

function mgs:v5.1.0/multiplayer/custom/fav_count_update

execute if score #fav_found mgs.data matches 1 run tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.removed_from_favorites","color":"yellow"}]
execute if score #fav_found mgs.data matches 0 run tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.added_to_favorites","color":"green"}]

# Reopen the Marketplace with the update.
function mgs:v5.1.0/multiplayer/marketplace/browse

