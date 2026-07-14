
#> mgs:v5.1.0/multiplayer/pickup_dropped_weapon
#
# @executed	as @n[tag=mgs.mp_drop_new]
#
# @within	mgs:v5.1.0/multiplayer/drop_held_weapon {run:"function mgs:v5.1.0/multiplayer/pickup_dropped_weapon",executor:"source"} [ as @n[tag=mgs.mp_drop_new] ]
#

execute unless score @s mgs.mp.in_game matches 1 run return fail
tag @s add mgs.mp_drop_picker
execute at @e[tag=bs.interaction.target] run function mgs:v5.1.0/multiplayer/pickup_collect
tag @s remove mgs.mp_drop_picker

