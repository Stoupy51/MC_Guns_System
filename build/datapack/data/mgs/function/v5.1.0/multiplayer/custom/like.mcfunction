
#> mgs:v5.1.0/multiplayer/custom/like
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# The trigger value carries the loadout id.
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 30000

# Mark it in the player's liked[], unless already there.
data modify storage mgs:temp _pd_src set from storage mgs:multiplayer player_data
data modify storage mgs:multiplayer player_data set value []
scoreboard players set #already_liked mgs.data 0
execute if data storage mgs:temp _pd_src[0] run function mgs:v5.1.0/multiplayer/custom/like_pd_rebuild

# Then raise the loadout's like count.
execute if score #already_liked mgs.data matches 0 run function mgs:v5.1.0/multiplayer/custom/like_increment_setup

execute if score #already_liked mgs.data matches 0 run tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.loadout_liked","color":"green"}]
execute if score #already_liked mgs.data matches 1 run tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_already_liked_this_loadout","color":"yellow"}]

function mgs:v5.1.0/multiplayer/marketplace/browse

