
#> stoupgun:v5.0.0/kicks/main
#
# @within	stoupgun:v5.0.0/right_click/handle
#

# Extract kick type & pick random value between 1 and 5
scoreboard players set #kick stoupgun.data 0
execute store result score #kick stoupgun.data run data get storage stoupgun:gun stats.kick
execute store result score #random stoupgun.data run random value 1..5

# Switch case
execute if score #kick stoupgun.data matches ..0 run function stoupgun:v5.0.0/kicks/type_0
execute if score #kick stoupgun.data matches 1 run function stoupgun:v5.0.0/kicks/type_1
execute if score #kick stoupgun.data matches 2 run function stoupgun:v5.0.0/kicks/type_2
execute if score #kick stoupgun.data matches 3 run function stoupgun:v5.0.0/kicks/type_3
execute if score #kick stoupgun.data matches 4 run function stoupgun:v5.0.0/kicks/type_4
execute if score #kick stoupgun.data matches 5.. run function stoupgun:v5.0.0/kicks/type_5

