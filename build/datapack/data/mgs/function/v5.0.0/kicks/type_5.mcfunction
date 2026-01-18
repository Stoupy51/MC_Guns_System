
#> mgs:v5.0.0/kicks/type_5
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/kicks/main
#

execute if score #has_vehicle mgs.data matches 0 if score #random mgs.data matches 1 run tp @s ~ ~ ~ ~-0.17 ~-2.5
execute if score #has_vehicle mgs.data matches 0 if score #random mgs.data matches 2 run tp @s ~ ~ ~ ~-0.06 ~-2.5
execute if score #has_vehicle mgs.data matches 0 if score #random mgs.data matches 3 run tp @s ~ ~ ~ ~-0.0 ~-2.5
execute if score #has_vehicle mgs.data matches 0 if score #random mgs.data matches 4 run tp @s ~ ~ ~ ~0.06 ~-2.5
execute if score #has_vehicle mgs.data matches 0 if score #random mgs.data matches 5 run tp @s ~ ~ ~ ~0.17 ~-2.5
execute if score #has_vehicle mgs.data matches 1 if score #random mgs.data matches 1 run rotate @s ~-0.17 ~-2.5
execute if score #has_vehicle mgs.data matches 1 if score #random mgs.data matches 2 run rotate @s ~-0.06 ~-2.5
execute if score #has_vehicle mgs.data matches 1 if score #random mgs.data matches 3 run rotate @s ~-0.0 ~-2.5
execute if score #has_vehicle mgs.data matches 1 if score #random mgs.data matches 4 run rotate @s ~0.06 ~-2.5
execute if score #has_vehicle mgs.data matches 1 if score #random mgs.data matches 5 run rotate @s ~0.17 ~-2.5

