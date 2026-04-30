
#> mgs:v5.0.0/zombies/mystery_box/check_owned_result
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/reroll_owned with storage mgs:zombies mystery_box.result
#
# @args		weapon_id (unknown)
#

scoreboard players set #mb_owned mgs.data 0
$execute if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1
$execute if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1
$execute if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}] run scoreboard players set #mb_owned mgs.data 1

# Also treat as owned if Ray Gun cap (max 2 players) is reached and result is Ray Gun (special case to limit 2 Ray Guns per game)
execute if score #mb_owned mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/check_ray_gun_cap

