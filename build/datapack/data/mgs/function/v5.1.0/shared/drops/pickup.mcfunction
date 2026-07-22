
#> mgs:v5.1.0/shared/drops/pickup
#
# @executed	as @n[tag=mgs.drop_new]
#
# @within	mgs:v5.1.0/shared/drops/spawn {run:"function mgs:v5.1.0/shared/drops/pickup",executor:"source"} [ as @n[tag=mgs.drop_new] ]
#

execute unless score @s mgs.mp.in_game matches 1 unless score @s mgs.mi.in_game matches 1 run return fail
execute store result score #pick_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #pick_sel mgs.data matches 1..2 run return fail
execute unless items entity @s weapon.mainhand *[custom_data~{mgs:{gun:true}}] run return fail
execute if data entity @s SelectedItem.components."minecraft:custom_data".mgs.stats.grenade_type run return fail
execute at @e[tag=bs.interaction.target] run function mgs:v5.1.0/shared/drops/collect

