
#> mgs:v5.0.1/multiplayer/custom/edit
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

# Extract loadout ID from trigger value
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 70000

# Launch a fresh editor flow, then mark it as targeting this loadout
# (editor/start resets edit_target to 0, so the target is set after)
function mgs:v5.0.1/multiplayer/editor/start
scoreboard players operation @s mgs.mp.edit_target = #loadout_id mgs.data

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.editing_loadout_walk_through_the_steps_saving_will_overwrite_it_","color":"yellow"}]

