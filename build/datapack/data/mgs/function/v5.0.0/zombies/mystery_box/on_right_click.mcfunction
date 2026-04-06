
#> mgs:v5.0.0/zombies/mystery_box/on_right_click
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/setup_pos_iter {run:"function mgs:v5.0.0/zombies/mystery_box/on_right_click",executor:"source"} [ as @n[tag=mgs.mb_new] ]
#

# Only respond if this is the active mystery box
execute unless entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run return fail

# Check game is active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# If box is moving: deny
execute if score #mb_move_timer mgs.data matches 1.. run return run function mgs:v5.0.0/zombies/mystery_box/deny_moving

# If result is ready: collect
execute if data storage mgs:zombies mystery_box{ready:true} run return run function mgs:v5.0.0/zombies/mystery_box/collect

# If already spinning: inform player
execute if data storage mgs:zombies mystery_box{spinning:true} run return run function mgs:v5.0.0/zombies/mystery_box/deny_already_in_use

# Otherwise: try to use (buy)
function mgs:v5.0.0/zombies/mystery_box/try_use

