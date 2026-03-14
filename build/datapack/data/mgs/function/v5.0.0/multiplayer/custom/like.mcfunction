
#> mgs:v5.0.0/multiplayer/custom/like
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1200

# Step 1: Check if already liked in our player_data, and add to liked[] if not
data modify storage mgs:temp _pd_src set from storage mgs:multiplayer player_data
data modify storage mgs:multiplayer player_data set value []
scoreboard players set #already_liked mgs.data 0
execute if data storage mgs:temp _pd_src[0] run function mgs:v5.0.0/multiplayer/custom/like_pd_rebuild

# Step 2: If not already liked, increment like counter on the loadout
execute if score #already_liked mgs.data matches 0 run function mgs:v5.0.0/multiplayer/custom/like_increment_setup

# Notify
execute if score #already_liked mgs.data matches 0 run tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.loadout_liked","color":"green"}]
execute if score #already_liked mgs.data matches 1 run tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_already_liked_this_loadout","color":"yellow"}]

# Reopen Marketplace dialog with updated data
function mgs:v5.0.0/multiplayer/marketplace/browse

