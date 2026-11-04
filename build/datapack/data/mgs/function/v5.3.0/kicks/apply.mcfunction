
#> mgs:v5.3.0/kicks/apply
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/kicks/main
#

execute if score #kick mgs.data matches ..0 run function mgs:v5.3.0/kicks/type_0
execute if score #kick mgs.data matches 1 run function mgs:v5.3.0/kicks/type_1
execute if score #kick mgs.data matches 2 run function mgs:v5.3.0/kicks/type_2
execute if score #kick mgs.data matches 3 run function mgs:v5.3.0/kicks/type_3
execute if score #kick mgs.data matches 4 run function mgs:v5.3.0/kicks/type_4
execute if score #kick mgs.data matches 5.. run function mgs:v5.3.0/kicks/type_5

