
#> mgs:v5.0.0/zombies/mystery_box/capture_collected_name
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/collect with storage mgs:zombies mystery_box.result
#
# @args		weapon_id (unknown)
#

data modify storage mgs:temp _mb_collected_name set value [{"text":"$(weapon_id)","color":"gold"}]
scoreboard players set #mb_name_found mgs.data 0

$execute if score #mb_name_found mgs.data matches 0 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/mystery_box/capture_collected_name_slot {slot:"hotbar.1"}
$execute if score #mb_name_found mgs.data matches 0 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/mystery_box/capture_collected_name_slot {slot:"hotbar.2"}
$execute if score #mb_name_found mgs.data matches 0 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run function mgs:v5.0.0/zombies/mystery_box/capture_collected_name_slot {slot:"hotbar.3"}

