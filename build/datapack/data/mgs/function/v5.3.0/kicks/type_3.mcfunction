
#> mgs:v5.3.0/kicks/type_3
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/kicks/apply
#

execute if score #random mgs.data matches 1 run rotate @s ~-0.13 ~-1.5
execute if score #random mgs.data matches 2 run rotate @s ~-0.06 ~-1.5
execute if score #random mgs.data matches 3 run rotate @s ~-0.0 ~-1.5
execute if score #random mgs.data matches 4 run rotate @s ~0.06 ~-1.5
execute if score #random mgs.data matches 5 run rotate @s ~0.13 ~-1.5

