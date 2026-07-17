
#> mgs:v5.1.0/multiplayer/pickup_dropped_weapon
#
# @executed	as @n[tag=mgs.mp_drop_new]
#
# @within	mgs:v5.1.0/multiplayer/drop_spawn {run:"function mgs:v5.1.0/multiplayer/pickup_dropped_weapon",executor:"source"} [ as @n[tag=mgs.mp_drop_new] ]
#

execute unless score @s mgs.mp.in_game matches 1 run return fail
execute store result score #pick_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #pick_sel mgs.data matches 0..1 run return fail
execute unless items entity @s weapon.mainhand *[custom_data~{mgs:{gun:true}}] run return fail
execute if data entity @s SelectedItem.components."minecraft:custom_data".mgs.stats.grenade_type run return fail
tag @s add mgs.mp_drop_picker
execute at @e[tag=bs.interaction.target] run function mgs:v5.1.0/multiplayer/pickup_collect
tag @s remove mgs.mp_drop_picker

