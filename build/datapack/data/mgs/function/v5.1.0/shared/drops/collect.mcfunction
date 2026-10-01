
#> mgs:v5.1.0/shared/drops/collect
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/shared/drops/pickup [ at @e[tag=bs.interaction.target] ]
#

execute unless entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] run return fail
execute store success score #pick_g0 mgs.data if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}]
execute store success score #pick_g1 mgs.data if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}]

# Without Overkill a pickup cannot leave two primaries.
scoreboard players set #pick_deny mgs.data 0
function mgs:v5.1.0/shared/drops/overkill_check
execute if score #pick_deny mgs.data matches 1 run return fail

# Death drops hand their embedded spare magazine over and lose it.
execute if data entity @n[type=minecraft:item_display,tag=mgs.dropped_gun,distance=..3] item.components."minecraft:custom_data".mgs.drop_mag run function mgs:v5.1.0/shared/drops/give_mag

execute if score #pick_g0 mgs.data matches 1 if score #pick_g1 mgs.data matches 1 run return run function mgs:v5.1.0/shared/drops/swap
function mgs:v5.1.0/shared/drops/take

