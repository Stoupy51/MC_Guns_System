
#> mgs:v5.1.0/kicks/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/right_click
#

# Extract kick type & pick random value between 1 and 5
scoreboard players set #kick mgs.data 0
execute store result score #kick mgs.data run data get storage mgs:gun all.stats.kick
execute store result score #random mgs.data run random value 1..5

# Check if player is riding a vehicle - if so, use /rotate instead of /tp to avoid dismounting
scoreboard players set #has_vehicle mgs.data 0
execute on vehicle run scoreboard players set #has_vehicle mgs.data 1

# Deadshot Daiquiri (zombies perk): route to the reduced-recoil (65%) kick variants
execute if score @s mgs.special.deadshot matches 1 run return run function mgs:v5.1.0/kicks/apply_ds

# Switch case
function mgs:v5.1.0/kicks/apply

