
#> mgs:v5.0.0/multiplayer/editor/perks_done
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

scoreboard players set @s mgs.mp.edit_step 10
# Show confirmation dialog
function mgs:v5.0.0/multiplayer/editor/show_confirm with storage mgs:temp editor

