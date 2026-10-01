
#> mgs:v5.1.0/multiplayer/custom/edit
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# The trigger value carries the loadout id.
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 70000

scoreboard players operation @s mgs.mp.edit_target = #loadout_id mgs.data

# Empty state first, then the loadout's saved editor_state if any.
function mgs:v5.1.0/multiplayer/editor/init_state
data modify storage mgs:temp _find_iter set from storage mgs:multiplayer custom_loadouts
scoreboard players set #edit_found mgs.data 0
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.1.0/multiplayer/custom/edit_load_iter

# Loadouts saved before editor_state cannot be pre-filled.
execute if score #edit_found mgs.data matches 0 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.this_loadout_predates_editing_support_rebuild_it_from_scratch_sa","color":"yellow"}]

# Points are recomputed from the loaded state.
function mgs:v5.1.0/multiplayer/editor/hub

