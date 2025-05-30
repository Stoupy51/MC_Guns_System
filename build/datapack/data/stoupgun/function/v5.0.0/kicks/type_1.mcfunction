
#> stoupgun:v5.0.0/kicks/type_1
#
# @within	stoupgun:v5.0.0/kicks/main
#

execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 1 run tp @s ~ ~ ~ ~-0.08 ~-0.5
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 2 run tp @s ~ ~ ~ ~-0.03 ~-0.5
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 3 run tp @s ~ ~ ~ ~-0.0 ~-0.5
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 4 run tp @s ~ ~ ~ ~0.03 ~-0.5
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 5 run tp @s ~ ~ ~ ~0.08 ~-0.5
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 1 run rotate @s ~-0.08 ~-0.5
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 2 run rotate @s ~-0.03 ~-0.5
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 3 run rotate @s ~-0.0 ~-0.5
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 4 run rotate @s ~0.03 ~-0.5
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 5 run rotate @s ~0.08 ~-0.5

