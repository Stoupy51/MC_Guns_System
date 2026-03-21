
#> mgs:v5.0.0/zombies/mystery_box/give_consumable_slot
#
# @within	mgs:v5.0.0/zombies/mystery_box/give_consumable_reserve {inventory:1,magazine_id:"$(magazine_id)",mag_count:$(mag_count)}
#			mgs:v5.0.0/zombies/mystery_box/give_consumable_reserve {inventory:2,magazine_id:"$(magazine_id)",mag_count:$(mag_count)}
#			mgs:v5.0.0/zombies/mystery_box/give_consumable_reserve {inventory:3,magazine_id:"$(magazine_id)",mag_count:$(mag_count)}
#
# @args		inventory (int)
#			magazine_id (string)
#			mag_count (int)
#

$loot replace entity @s inventory.$(inventory) loot mgs:i/$(magazine_id)
$scoreboard players set #bullets mgs.data $(mag_count)
$item modify entity @s inventory.$(inventory) mgs:v5.0.0/set_consumable_count
$function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}
scoreboard players set #mb_mag_given mgs.data 1

