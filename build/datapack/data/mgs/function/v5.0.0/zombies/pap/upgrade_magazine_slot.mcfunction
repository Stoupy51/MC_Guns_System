
#> mgs:v5.0.0/zombies/pap/upgrade_magazine_slot
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.0"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.1"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.2"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.3"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.4"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.5"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.6"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.7"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"hotbar.8"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"weapon.offhand"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.0"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.1"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.2"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.3"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.4"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.5"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.6"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.7"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.8"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.9"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.10"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.11"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.12"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.13"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.14"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.15"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.16"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.17"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.18"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.19"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.20"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.21"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.22"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.23"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.24"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.25"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"inventory.26"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"player.cursor"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"player.crafting.0"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"player.crafting.1"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"player.crafting.2"}
#			mgs:v5.0.0/zombies/pap/pap_upgrade_magazines {slot:"player.crafting.3"}
#
# @args		slot (string)
#

# Set magazine capacity and remaining to weapon capacity x 8
execute store result storage mgs:temp zb_item_stats.capacity int 1 run scoreboard players get #pap_mag_cap mgs.data
execute store result storage mgs:temp zb_item_stats.remaining_bullets int 1 run scoreboard players get #pap_mag_cap mgs.data

# Apply new stats to magazine
$item modify entity @s $(slot) mgs:v5.0.0/zb_item_stats

# Update magazine lore
data modify storage mgs:temp capacity set from storage mgs:temp zb_item_stats.capacity
scoreboard players operation #bullets mgs.data = #pap_mag_cap mgs.data
$function mgs:v5.0.0/ammo/modify_mag_lore {slot:"$(slot)"}

# Restore full magazine model (read actual item_model from the magazine)
$data modify storage mgs:temp refill.slot set value "$(slot)"
data modify storage mgs:temp refill.base_weapon set from storage mgs:temp _pap_extract.stats.base_weapon
tag @s add mgs.pap_extracting_mag
$execute summon item_display run function mgs:v5.0.0/zombies/pap/extract_mag_model {slot:"$(slot)"}
tag @s remove mgs.pap_extracting_mag
function mgs:v5.0.0/zombies/bonus/set_full_mag_model with storage mgs:temp refill

