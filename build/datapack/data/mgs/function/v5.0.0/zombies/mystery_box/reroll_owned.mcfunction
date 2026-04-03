
#> mgs:v5.0.0/zombies/mystery_box/reroll_owned
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use
#			mgs:v5.0.0/zombies/mystery_box/reroll_owned
#

scoreboard players set #mb_owned mgs.data 0
execute if data storage mgs:zombies mystery_box.result.weapon_id run function mgs:v5.0.0/zombies/mystery_box/check_owned_result with storage mgs:zombies mystery_box.result
execute if score #mb_owned mgs.data matches 1 if score #mb_reroll mgs.data matches ..19 run scoreboard players add #mb_reroll mgs.data 1
execute if score #mb_owned mgs.data matches 1 if score #mb_reroll mgs.data matches ..19 run function mgs:v5.0.0/zombies/mystery_box/pick_random_result
execute if score #mb_owned mgs.data matches 1 if score #mb_reroll mgs.data matches ..19 run function mgs:v5.0.0/zombies/mystery_box/reroll_owned

