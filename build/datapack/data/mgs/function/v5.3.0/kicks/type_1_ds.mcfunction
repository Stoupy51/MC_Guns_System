
#> mgs:v5.3.0/kicks/type_1_ds
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/kicks/apply_ds
#

execute if score #random mgs.data matches 1 run rotate @s ~-0.052 ~-0.325
execute if score #random mgs.data matches 2 run rotate @s ~-0.0195 ~-0.325
execute if score #random mgs.data matches 3 run rotate @s ~-0.0 ~-0.325
execute if score #random mgs.data matches 4 run rotate @s ~0.0195 ~-0.325
execute if score #random mgs.data matches 5 run rotate @s ~0.052 ~-0.325

