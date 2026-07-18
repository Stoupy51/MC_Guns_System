
#> mgs:v5.1.0/zombies/mystery_box/on_left_click
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.1.0/zombies/mystery_box/setup_pos_iter {run:"function mgs:v5.1.0/zombies/mystery_box/on_left_click",executor:"source"} [ as @n[tag=mgs.mb_new] ]
#

# Plain left click is a normal swing, only sneaking means "share this"
execute unless predicate mgs:v5.1.0/is_sneaking run return fail
execute unless data storage mgs:zombies game{state:"active"} run return fail
execute at @n[tag=bs.interaction.target] run function mgs:v5.1.0/zombies/mystery_box/share_at_box

