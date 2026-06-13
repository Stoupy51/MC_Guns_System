
#> mgs:v5.0.1/multiplayer/custom/edit
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 70000

# Mark the editor active and targeting this loadout
scoreboard players set @s mgs.mp.edit_step 1
scoreboard players operation @s mgs.mp.edit_target = #loadout_id mgs.data

# Start from an empty state, then overwrite it with the loadout's saved editor_state (if any)
function mgs:v5.0.1/multiplayer/editor/init_state
data modify storage mgs:temp _find_iter set from storage mgs:multiplayer custom_loadouts
scoreboard players set #edit_found mgs.data 0
execute if data storage mgs:temp _find_iter[0] run function mgs:v5.0.1/multiplayer/custom/edit_load_iter

# Legacy loadouts (saved before editor_state existed) can't be pre-filled — warn the player
execute if score #edit_found mgs.data matches 0 run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.this_loadout_predates_editing_support_rebuild_it_from_scratch_sa","color":"yellow"}]

# Open the hub (points recompute from the loaded state)
function mgs:v5.0.1/multiplayer/editor/hub

