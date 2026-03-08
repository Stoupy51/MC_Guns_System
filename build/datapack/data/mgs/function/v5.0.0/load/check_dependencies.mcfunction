
#> mgs:v5.0.0/load/check_dependencies
#
# @within	mgs:v5.0.0/load/secondary
#

## Check if MC Guns System is loadable (dependencies)
scoreboard players set #dependency_error mgs.data 0
execute if score #dependency_error mgs.data matches 0 unless score #realistic_explosion.major load.status matches 1.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score #realistic_explosion.major load.status matches 1 unless score #realistic_explosion.minor load.status matches 2.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.block.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.block.major load.status matches 4 unless score $bs.block.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.dump.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.dump.major load.status matches 4 unless score $bs.dump.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.hitbox.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.hitbox.major load.status matches 4 unless score $bs.hitbox.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.interaction.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.interaction.major load.status matches 4 unless score $bs.interaction.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.math.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.math.major load.status matches 4 unless score $bs.math.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.move.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.move.major load.status matches 4 unless score $bs.move.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.position.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.position.major load.status matches 4 unless score $bs.position.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.random.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.random.major load.status matches 4 unless score $bs.random.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.raycast.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.raycast.major load.status matches 4 unless score $bs.raycast.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.sidebar.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.sidebar.major load.status matches 4 unless score $bs.sidebar.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 unless score $bs.view.major load.status matches 4.. run scoreboard players set #dependency_error mgs.data 1
execute if score #dependency_error mgs.data matches 0 if score $bs.view.major load.status matches 4 unless score $bs.view.minor load.status matches 0.. run scoreboard players set #dependency_error mgs.data 1

