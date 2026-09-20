
#> mgs:v5.1.0/zombies/mystery_box/on_hover
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.1.0/zombies/mystery_box/setup_pos_iter {run:"function mgs:v5.1.0/zombies/mystery_box/on_hover",executor:"source"} [ as @n[tag=mgs.mb_new] ]
#

# Only over a usable box (active, any box during a Fire Sale, or a box with a pull in progress)
scoreboard players set #mb_usable mgs.data 0
execute if entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run scoreboard players set #mb_usable mgs.data 1
execute if score #zb_fire_sale_timer mgs.data matches 1.. if entity @e[tag=bs.interaction.target,tag=mgs.mb_fs_active] run scoreboard players set #mb_usable mgs.data 1
execute at @n[tag=bs.interaction.target] if entity @n[tag=mgs.mb_display,distance=..3] run scoreboard players set #mb_usable mgs.data 1
execute if score #mb_usable mgs.data matches 0 run return fail
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Active box mid-move
execute if score #mb_move_timer mgs.data matches 1.. if entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run return run function mgs:v5.1.0/zombies/mystery_box/hud_moving

# This box's pull state (at the box)
execute at @n[tag=bs.interaction.target] run function mgs:v5.1.0/zombies/mystery_box/hover_at_box

