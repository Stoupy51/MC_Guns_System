
#> mgs:v5.4.0/kicks/apply_ds
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/kicks/tick
#

execute if score @s mgs.kick matches 0 run function mgs:v5.4.0/kicks/type_0_ds
execute if score @s mgs.kick matches 1 run function mgs:v5.4.0/kicks/type_1_ds
execute if score @s mgs.kick matches 2 run function mgs:v5.4.0/kicks/type_2_ds
execute if score @s mgs.kick matches 3 run function mgs:v5.4.0/kicks/type_3_ds
execute if score @s mgs.kick matches 4 run function mgs:v5.4.0/kicks/type_4_ds
execute if score @s mgs.kick matches 5 run function mgs:v5.4.0/kicks/type_5_ds

