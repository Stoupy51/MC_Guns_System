
#> mgs:v5.4.2/multiplayer/custom/toggle_visibility
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/config/process
#

# The trigger value carries the loadout id.
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 50000

# Rebuild the list, toggling the matching entry.
data modify storage mgs:temp _del_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []
execute if data storage mgs:temp _del_src[0] run function mgs:v5.4.2/multiplayer/custom/toggle_vis_rebuild

tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.loadout_visibility_toggled","fallback":"Loadout visibility toggled","color":"green"}]

function mgs:v5.4.2/multiplayer/my_loadouts/browse

