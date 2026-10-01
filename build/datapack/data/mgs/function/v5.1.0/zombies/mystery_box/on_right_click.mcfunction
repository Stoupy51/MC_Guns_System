
#> mgs:v5.1.0/zombies/mystery_box/on_right_click
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.1.0/zombies/mystery_box/setup_pos_iter {run:"function mgs:v5.1.0/zombies/mystery_box/on_right_click",executor:"source"} [ as @n[tag=mgs.mb_new] ]
#

# Usable: the active box, any box during a Fire Sale, or a box with a pull in progress (so a buyer can always collect).
scoreboard players set #mb_usable mgs.data 0
execute if entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run scoreboard players set #mb_usable mgs.data 1
execute if score #zb_fire_sale_timer mgs.data matches 1.. if entity @e[tag=bs.interaction.target,tag=mgs.mb_fs_active] run scoreboard players set #mb_usable mgs.data 1
execute at @n[tag=bs.interaction.target] if entity @n[tag=mgs.mb_display,distance=..3] run scoreboard players set #mb_usable mgs.data 1
execute if score #mb_usable mgs.data matches 0 run return fail

execute unless data storage mgs:zombies game{state:"active"} run return fail

# The active box can be moving.
execute if score #mb_move_timer mgs.data matches 1.. if entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.the_mystery_box_is_moving","color":"yellow"}'}

# Dispatched at the box position.
scoreboard players operation #cur_box mgs.data = @n[tag=bs.interaction.target] mgs.mb.box
execute at @n[tag=bs.interaction.target] run function mgs:v5.1.0/zombies/mystery_box/box_click

