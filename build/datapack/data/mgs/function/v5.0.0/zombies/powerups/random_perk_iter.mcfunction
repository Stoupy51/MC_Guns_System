
#> mgs:v5.0.0/zombies/powerups/random_perk_iter
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/activate/random_perk
#			mgs:v5.0.0/zombies/powerups/random_perk_iter
#

# Safety counter: prevent infinite recursion (max 6 iterations)
scoreboard players add #pu_perk_tries mgs.data 1
execute if score #pu_perk_tries mgs.data matches 6.. run return 0

# Stop if a perk has already been applied in a previous iteration
execute if score #pu_perk_applied mgs.data matches 1 run return 0

# Try the perk at the current roll index; each try_perk function sets #pu_perk_applied on success
execute if score #pu_perk_roll mgs.data matches 0 run function mgs:v5.0.0/zombies/powerups/try_perk/juggernog
execute if score #pu_perk_applied mgs.data matches 1 run return 0
execute if score #pu_perk_roll mgs.data matches 1 run function mgs:v5.0.0/zombies/powerups/try_perk/speed_cola
execute if score #pu_perk_applied mgs.data matches 1 run return 0
execute if score #pu_perk_roll mgs.data matches 2 run function mgs:v5.0.0/zombies/powerups/try_perk/double_tap
execute if score #pu_perk_applied mgs.data matches 1 run return 0
execute if score #pu_perk_roll mgs.data matches 3 run function mgs:v5.0.0/zombies/powerups/try_perk/quick_revive
execute if score #pu_perk_applied mgs.data matches 1 run return 0
execute if score #pu_perk_roll mgs.data matches 4 run function mgs:v5.0.0/zombies/powerups/try_perk/mule_kick
execute if score #pu_perk_applied mgs.data matches 1 run return 0

# No perk applied at this index (already owned): advance roll and recurse
scoreboard players add #pu_perk_roll mgs.data 1
execute if score #pu_perk_roll mgs.data matches 5.. run scoreboard players set #pu_perk_roll mgs.data 0
function mgs:v5.0.0/zombies/powerups/random_perk_iter

