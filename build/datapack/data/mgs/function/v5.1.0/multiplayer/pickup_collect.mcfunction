
#> mgs:v5.1.0/multiplayer/pickup_collect
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/multiplayer/pickup_dropped_weapon [ at @e[tag=bs.interaction.target] ]
#

execute unless entity @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] run return fail
execute store success score #pick_g0 mgs.data if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}]
execute store success score #pick_g1 mgs.data if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}]

# Without the Overkill perk, a pickup may not leave the player with two primary weapons
scoreboard players set #pick_deny mgs.data 0
function mgs:v5.1.0/multiplayer/pickup_overkill_check
execute if score #pick_deny mgs.data matches 1 run return fail

# Death drops carry a spare magazine inside the gun's custom data: hand it over and strip it from the gun
execute if data entity @n[type=minecraft:item_display,tag=mgs.mp_dropped_gun,distance=..3] item.components."minecraft:custom_data".mgs.drop_mag run function mgs:v5.1.0/multiplayer/pickup_give_mag

execute if score #pick_g0 mgs.data matches 1 if score #pick_g1 mgs.data matches 1 run return run function mgs:v5.1.0/multiplayer/pickup_swap
function mgs:v5.1.0/multiplayer/pickup_take

