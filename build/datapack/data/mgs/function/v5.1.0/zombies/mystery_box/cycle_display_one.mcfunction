
#> mgs:v5.1.0/zombies/mystery_box/cycle_display_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/cycle_step_one
#

data modify storage bs:in random.weighted_choice.options set from storage mgs:zombies mystery_box_pool
data modify storage bs:in random.weighted_choice.weights set from storage mgs:zombies mystery_box_weights
function #bs.random:weighted_choice
data modify storage mgs:temp _mb_cycle_item set from storage bs:out random.weighted_choice
execute if data storage mgs:temp _mb_cycle_item.weapon_id run function mgs:v5.1.0/zombies/mystery_box/cycle_display_weapon_one with storage mgs:temp _mb_cycle_item
execute unless data storage mgs:temp _mb_cycle_item.weapon_id run data modify entity @s item set from storage mgs:temp _mb_cycle_item.display_item

