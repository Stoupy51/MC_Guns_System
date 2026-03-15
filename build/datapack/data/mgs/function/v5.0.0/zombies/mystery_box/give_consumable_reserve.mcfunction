
#> mgs:v5.0.0/zombies/mystery_box/give_consumable_reserve
#
# @within	mgs:v5.0.0/zombies/mystery_box/default_give/ak47 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m16a4 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/famas with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/aug with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m4a1 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/fnfal with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/g3a3 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/scar17 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mp5 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mp7 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mac10 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/ppsh41 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/sten with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m249 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/rpk with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/svd with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m82 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/mosin with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m24 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/spas12 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m500 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m590 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/rpg7 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m1911 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/m9 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/deagle with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/makarov with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/glock17 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/glock18 with storage mgs:temp _wb_weapon
#			mgs:v5.0.0/zombies/mystery_box/default_give/vz61 with storage mgs:temp _wb_weapon
#
# @args		weapon_id (string)
#			mag_id (string)
#			mag_count (int)
#

scoreboard players set #mb_mag_given mgs.data 0

$execute if score #mb_mag_given mgs.data matches 0 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/mystery_box/give_consumable_slot {inventory:1,mag_id:"$(mag_id)",mag_count:$(mag_count)}
$execute if score #mb_mag_given mgs.data matches 0 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/mystery_box/give_consumable_slot {inventory:2,mag_id:"$(mag_id)",mag_count:$(mag_count)}
$execute if score #mb_mag_given mgs.data matches 0 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/mystery_box/give_consumable_slot {inventory:3,mag_id:"$(mag_id)",mag_count:$(mag_count)}

