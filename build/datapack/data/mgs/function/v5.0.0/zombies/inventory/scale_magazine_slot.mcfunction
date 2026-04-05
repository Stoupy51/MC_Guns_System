
#> mgs:v5.0.0/zombies/inventory/scale_magazine_slot
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/inventory/give_starting_loadout {slot:"inventory.1",index:1,remaining_multiplier:0.5}
#			mgs:v5.0.0/zombies/wallbuys/give_to_slot {slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}
#			mgs:v5.0.0/zombies/wallbuys/reload_pair {slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}
#			mgs:v5.0.0/zombies/wallbuys/replace_pair {slot:"inventory.$(inventory)",index:$(inventory),remaining_multiplier:1}
#
# @args		index (int)
#			remaining_multiplier (double)
#			slot (string)
#

# Read capacity from the paired weapon at hotbar.$(index) (inventory.N always pairs with hotbar.N)
tag @s add mgs.zb_scaling_mag
$execute summon item_display run function mgs:v5.0.0/zombies/inventory/read_capacity {slot:"hotbar.$(index)",multiplier:6}
tag @s remove mgs.zb_scaling_mag

# Write capacity and starting ammo into custom_data
execute store result storage mgs:temp zb_item_stats.capacity int 1 run scoreboard players get #zb_cap mgs.data
$execute store result storage mgs:temp zb_item_stats.remaining_bullets int $(remaining_multiplier) run scoreboard players get #zb_cap mgs.data
$item modify entity @s $(slot) mgs:v5.0.0/zb_item_stats

# Mark as zombies-converted (consumable=2b): ammo.py reads remaining_bullets instead of stack count.
$item modify entity @s $(slot) mgs:v5.0.0/zb_mark_converted

# Force count to 1 (consumable magazines used stack count as ammo, now using custom_data)
scoreboard players set #bullets mgs.data 1
$item modify entity @s $(slot) mgs:v5.0.0/set_consumable_count

# Update magazine lore to show new ammo count
data modify storage mgs:temp capacity set from storage mgs:temp zb_item_stats.capacity
execute store result score #bullets mgs.data run data get storage mgs:temp zb_item_stats.remaining_bullets
$function mgs:v5.0.0/ammo/modify_mag_lore {slot:"$(slot)"}

