
#> stoupgun:v5.0.0/load/check_dependencies
#
# @within	stoupgun:v5.0.0/load/secondary
#

## Check if StoupGun is loadable (dependencies)
scoreboard players set #dependency_error stoupgun.data 0
execute if score #dependency_error stoupgun.data matches 0 unless score $bs.raycast.major load.status matches 3.. run scoreboard players set #dependency_error stoupgun.data 1
execute if score #dependency_error stoupgun.data matches 0 if score $bs.raycast.major load.status matches 3 unless score $bs.raycast.minor load.status matches 0.. run scoreboard players set #dependency_error stoupgun.data 1
execute if score #dependency_error stoupgun.data matches 0 if score $bs.raycast.major load.status matches 3 if score $bs.raycast.minor load.status matches 0 unless score $bs.raycast.patch load.status matches 2.. run scoreboard players set #dependency_error stoupgun.data 1

