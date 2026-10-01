
#> mgs:v5.1.0/ammo/modify_mag_lore
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/inventory/process_slot {slot:"$(slot)"}
#			mgs:v5.1.0/zombies/bonus/refill_magazine {slot:"$(slot)"}
#			mgs:v5.1.0/zombies/inventory/scale_magazine_slot {slot:"$(slot)"}
#			mgs:v5.1.0/zombies/pap/upgrade_magazine_slot {slot:"$(slot)"}
#
# @args		slot (string)
#

# Target of the item_display.
tag @s add mgs.modify_mag_lore

$execute summon item_display run function mgs:v5.1.0/ammo/get_current_mag_lore {"slot":"$(slot)"}

scoreboard players set #index mgs.data 0
$execute if data storage mgs:temp copy[0] run function mgs:v5.1.0/ammo/search_mag_lore_loop {"slot":"$(slot)"}

tag @s remove mgs.modify_mag_lore

