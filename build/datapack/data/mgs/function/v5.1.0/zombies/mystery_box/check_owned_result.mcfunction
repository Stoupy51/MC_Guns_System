
#> mgs:v5.1.0/zombies/mystery_box/check_owned_result
#
# @within	mgs:v5.1.0/zombies/mystery_box/reroll_owned with storage mgs:zombies mystery_box.result
#
# @args		weapon_id (unknown)
#

scoreboard players set #mb_owned mgs.data 0
$execute if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1
$execute if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1
$execute if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1
# Holding any tactical (monkey bombs) counts as owned, so the box re-rolls.
$execute if items entity @s hotbar.6 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1

# At most 2 Ray Guns per game.
execute if score #mb_owned mgs.data matches 0 run function mgs:v5.1.0/zombies/mystery_box/check_ray_gun_cap

