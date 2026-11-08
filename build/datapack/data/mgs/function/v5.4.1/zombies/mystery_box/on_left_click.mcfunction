
#> mgs:v5.4.1/zombies/mystery_box/on_left_click
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/mystery_box/setup_pos_iter {run:"function mgs:v5.4.1/zombies/mystery_box/on_left_click",executor:"source"} [ as @n[tag=mgs.mb_new] ]
#

# A plain left click is a normal swing.
execute unless predicate mgs:v5.4.1/is_sneaking run return fail
execute unless data storage mgs:zombies game{state:"active"} run return fail
execute at @n[tag=bs.interaction.target] run function mgs:v5.4.1/zombies/mystery_box/share_at_box

