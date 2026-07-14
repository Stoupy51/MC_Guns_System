
#> mgs:v5.1.0/multiplayer/custom/delete
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Extract loadout ID from trigger value: id = trigger - 40000
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 40000

# Copy the list, rebuild without the deleted entry
data modify storage mgs:temp _del_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []

# Rebuild list, skipping the entry that matches both ID and owner (score-based)
scoreboard players set #del_removed mgs.data 0
execute if data storage mgs:temp _del_src[0] run function mgs:v5.1.0/multiplayer/custom/delete_filter

# Clear dangling references: if the deleted loadout was the default or active class, reset them
scoreboard players operation #del_neg_id mgs.data = #loadout_id mgs.data
scoreboard players operation #del_neg_id mgs.data *= #minus_one mgs.data
execute if score #del_removed mgs.data matches 1 if score @s mgs.mp.default = #loadout_id mgs.data run scoreboard players set @s mgs.mp.default 0
execute if score #del_removed mgs.data matches 1 if score @s mgs.mp.class = #del_neg_id mgs.data run scoreboard players set @s mgs.mp.class 0

# Notify
tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.loadout_deleted","color":"red"}]

# Reopen My Loadouts dialog with updated data
function mgs:v5.1.0/multiplayer/my_loadouts/browse

