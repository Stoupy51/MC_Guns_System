
#> mgs:v5.0.0/zombies/inventory/fix_grenade
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/check_slots
#

clear @s *[custom_data~{mgs:{gun:true,stats:{grenade_type:"frag"}}}]
data modify storage mgs:temp zb_item_stats set value {capacity:4,remaining_bullets:0}
loot replace entity @s hotbar.7 loot mgs:i/frag_grenade
item modify entity @s hotbar.7 mgs:v5.0.0/zb_item_stats

