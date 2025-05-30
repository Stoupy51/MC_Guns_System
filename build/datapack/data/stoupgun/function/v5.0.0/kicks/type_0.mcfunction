
#> stoupgun:v5.0.0/kicks/type_0
#
# @within	stoupgun:v5.0.0/kicks/main
#

execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 1 run tp @s ~ ~ ~ ~-0.05 ~-0.25
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 2 run tp @s ~ ~ ~ ~-0.025 ~-0.25
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 3 run tp @s ~ ~ ~ ~-0.0 ~-0.25
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 4 run tp @s ~ ~ ~ ~0.025 ~-0.25
execute if score #has_vehicle stoupgun.data matches 0 if score #random stoupgun.data matches 5 run tp @s ~ ~ ~ ~0.05 ~-0.25
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 1 run rotate @s ~-0.05 ~-0.25
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 2 run rotate @s ~-0.025 ~-0.25
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 3 run rotate @s ~-0.0 ~-0.25
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 4 run rotate @s ~0.025 ~-0.25
execute if score #has_vehicle stoupgun.data matches 1 if score #random stoupgun.data matches 5 run rotate @s ~0.05 ~-0.25

