
#> mgs:v5.0.0/zombies/mystery_box/cycle_display
#
# @within	mgs:v5.0.0/zombies/mystery_box/cycle_step
#

# Pick a random item from pool to display
data modify storage bs:in random.weighted_choice.options set from storage mgs:zombies mystery_box_pool
data modify storage bs:in random.weighted_choice.weights set from storage mgs:zombies mystery_box_weights
function #bs.random:weighted_choice
data modify storage mgs:temp _mb_cycle_item set from storage bs:out random.weighted_choice

# Apply the cycled item to the display entity.
execute if data storage mgs:temp _mb_cycle_item.weapon_id run function mgs:v5.0.0/zombies/mystery_box/cycle_display_weapon with storage mgs:temp _mb_cycle_item
execute unless data storage mgs:temp _mb_cycle_item.weapon_id run data modify entity @n[tag=mgs.mb_display] item set from storage mgs:temp _mb_cycle_item.display_item

