
#> mgs:v5.0.0/multiplayer/custom/delete
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value: id = trigger - 1300
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1300

# Copy the list, rebuild without the deleted entry
data modify storage mgs:temp _del_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []

# Rebuild list, skipping the entry that matches both ID and owner (score-based)
execute if data storage mgs:temp _del_src[0] run function mgs:v5.0.0/multiplayer/custom/delete_filter

# Notify
tellraw @s ["",{"translate": "mgs","color":"gold"},{"translate": "mgs.loadout_deleted","color":"green"}]

# Reopen My Loadouts dialog with updated data
function mgs:v5.0.0/multiplayer/my_loadouts/browse

