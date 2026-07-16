
#> mgs:v5.1.0/multiplayer/pickup_collect
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/multiplayer/pickup_dropped_weapon [ at @e[tag=bs.interaction.target] ]
#

execute unless entity @n[tag=mgs.mp_dropped_gun,distance=..3] run return fail
execute store success score #pick_g0 mgs.data if items entity @s hotbar.0 *[custom_data~{mgs:{gun:true}}]
execute store success score #pick_g1 mgs.data if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}]
execute if score #pick_g0 mgs.data matches 1 if score #pick_g1 mgs.data matches 1 run return run function mgs:v5.1.0/multiplayer/pickup_swap
function mgs:v5.1.0/multiplayer/pickup_take

