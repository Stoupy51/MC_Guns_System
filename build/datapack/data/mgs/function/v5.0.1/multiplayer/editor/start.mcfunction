
#> mgs:v5.0.1/multiplayer/editor/start
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/config/process
#

scoreboard players set @s mgs.mp.edit_step 1
# Default to creating a new loadout (custom/edit overrides this after calling start)
scoreboard players set @s mgs.mp.edit_target 0
function mgs:v5.0.1/multiplayer/editor/init_state
function mgs:v5.0.1/multiplayer/editor/hub

