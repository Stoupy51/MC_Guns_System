
#> mgs:v5.0.0/zombies/mystery_box/check_ray_gun_cap
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/check_owned_result
#

# Only applies when the result is ray_gun
execute unless data storage mgs:zombies mystery_box.result{weapon_id:"ray_gun"} run return fail

# Count ray_gun owners across all in-game players (cap = 2)
scoreboard players set #mb_ray_gun_owners mgs.data 0
execute as @a[scores={mgs.zb.in_game=1}] if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"ray_gun"}}}] run scoreboard players add #mb_ray_gun_owners mgs.data 1
execute as @a[scores={mgs.zb.in_game=1}] if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"ray_gun"}}}] run scoreboard players add #mb_ray_gun_owners mgs.data 1
execute as @a[scores={mgs.zb.in_game=1}] if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true,stats:{base_weapon:"ray_gun"}}}] run scoreboard players add #mb_ray_gun_owners mgs.data 1
execute if score #mb_ray_gun_owners mgs.data matches 2.. run scoreboard players set #mb_owned mgs.data 1

