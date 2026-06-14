
#> mgs:v5.0.1/zombies/mystery_box/on_right_click
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.1/zombies/mystery_box/setup_pos_iter {run:"function mgs:v5.0.1/zombies/mystery_box/on_right_click",executor:"source"} [ as @n[tag=mgs.mb_new] ]
#

# A box is usable if it's the active box, any box during a Fire Sale, or a box that still has a
# pull in progress (so a buyer can always collect/finish a pull even after a Fire Sale ended).
scoreboard players set #mb_usable mgs.data 0
execute if entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run scoreboard players set #mb_usable mgs.data 1
execute if score #zb_fire_sale_timer mgs.data matches 1.. if entity @e[tag=bs.interaction.target,tag=mgs.mb_fs_active] run scoreboard players set #mb_usable mgs.data 1
execute at @n[tag=bs.interaction.target] if entity @n[tag=mgs.mb_display,distance=..3] run scoreboard players set #mb_usable mgs.data 1
execute if score #mb_usable mgs.data matches 0 run return fail

# Check game is active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# The active box can be mid-move: deny
execute if score #mb_move_timer mgs.data matches 1.. if entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run return run function mgs:v5.0.1/zombies/mystery_box/deny_moving

# Capture the clicked box id, then dispatch at the box position
scoreboard players operation #cur_box mgs.data = @n[tag=bs.interaction.target] mgs.mb.box
execute at @n[tag=bs.interaction.target] run function mgs:v5.0.1/zombies/mystery_box/box_click

