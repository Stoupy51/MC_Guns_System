
#> mgs:v5.0.0/zombies/mystery_box/check_owned_result
#
# @within	mgs:v5.0.0/zombies/mystery_box/reroll_owned with storage mgs:zombies mystery_box.result
#
# @args		weapon_id (unknown)
#

scoreboard players set #mb_owned mgs.data 0
$execute if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1
$execute if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1
$execute if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1

