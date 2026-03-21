
#> mgs:v5.0.0/zombies/inventory/scale_magazine_slot
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/inventory/give_starting_loadout {slot:"inventory.1"}
#			mgs:v5.0.0/zombies/wallbuys/give_to_slot {slot:"inventory.$(inventory)"}
#			mgs:v5.0.0/zombies/wallbuys/reload_pair {slot:"inventory.$(inventory)"}
#			mgs:v5.0.0/zombies/wallbuys/replace_pair {slot:"inventory.$(inventory)"}
#
# @args		slot (string)
#

tag @s add mgs.zb_scaling_mag
$execute summon item_display run function mgs:v5.0.0/zombies/inventory/read_mag_capacity {slot:"$(slot)"}
tag @s remove mgs.zb_scaling_mag

# Store face-value capacity directly (no consumable x8 scaling needed).
execute store result storage mgs:temp zb_item_stats.capacity int 1 run scoreboard players get #zb_cap mgs.data

# Start at half capacity (floor).
scoreboard players set #zb_const mgs.data 2
scoreboard players operation #zb_cap mgs.data /= #zb_const mgs.data
execute store result storage mgs:temp zb_item_stats.remaining_bullets int 1 run scoreboard players get #zb_cap mgs.data

$item modify entity @s $(slot) mgs:v5.0.0/zb_item_stats

