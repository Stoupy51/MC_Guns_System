
#> mgs:v5.0.0/multiplayer/custom/toggle_visibility
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 1400

# Rebuild list with toggled visibility on the matching entry
data modify storage mgs:temp _del_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
execute if data storage mgs:temp _del_src[0] run function mgs:v5.0.0/multiplayer/custom/toggle_vis_rebuild

tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.loadout_visibility_toggled","color":"green"}]

# Reopen My Loadouts dialog with updated data
function mgs:v5.0.0/multiplayer/my_loadouts/browse

