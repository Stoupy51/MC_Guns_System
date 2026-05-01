
#> mgs:v5.0.0/zombies/powerups/dispatch_activate
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/do_pickup
#

execute if score #pu_type_pickup mgs.data matches 1 run function mgs:v5.0.0/zombies/powerups/activate/max_ammo
execute if score #pu_type_pickup mgs.data matches 2 run function mgs:v5.0.0/zombies/powerups/activate/insta_kill
execute if score #pu_type_pickup mgs.data matches 3 run function mgs:v5.0.0/zombies/powerups/activate/double_points
execute if score #pu_type_pickup mgs.data matches 4 run function mgs:v5.0.0/zombies/powerups/activate/carpenter
execute if score #pu_type_pickup mgs.data matches 5 run function mgs:v5.0.0/zombies/powerups/activate/unlimited_ammo
execute if score #pu_type_pickup mgs.data matches 6 run function mgs:v5.0.0/zombies/powerups/activate/nuke
execute if score #pu_type_pickup mgs.data matches 7 run function mgs:v5.0.0/zombies/powerups/activate/random_perk
execute if score #pu_type_pickup mgs.data matches 8 run function mgs:v5.0.0/zombies/powerups/activate/free_pap
execute if score #pu_type_pickup mgs.data matches 9 run function mgs:v5.0.0/zombies/powerups/activate/cash_drop

