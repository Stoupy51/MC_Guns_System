
#> mgs:v5.1.0/kicks/apply_ds
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/kicks/main
#

execute if score #kick mgs.data matches ..0 run function mgs:v5.1.0/kicks/type_0_ds
execute if score #kick mgs.data matches 1 run function mgs:v5.1.0/kicks/type_1_ds
execute if score #kick mgs.data matches 2 run function mgs:v5.1.0/kicks/type_2_ds
execute if score #kick mgs.data matches 3 run function mgs:v5.1.0/kicks/type_3_ds
execute if score #kick mgs.data matches 4 run function mgs:v5.1.0/kicks/type_4_ds
execute if score #kick mgs.data matches 5.. run function mgs:v5.1.0/kicks/type_5_ds

