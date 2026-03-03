
#> mgs:v5.0.0/multiplayer/custom/select
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value: id = trigger - 1000
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1000

# Store as active custom class (negative mp.class = custom loadout ID)
scoreboard players operation @s mgs.mp.class = #loadout_id mgs.data
scoreboard players operation @s mgs.mp.class *= #minus_one mgs.data

# Find the loadout name for notification
data modify storage mgs:temp _find_iter set from storage mgs:multiplayer custom_loadouts
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.0.0/multiplayer/custom/find_and_notify

