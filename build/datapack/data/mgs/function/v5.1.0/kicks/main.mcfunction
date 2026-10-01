
#> mgs:v5.1.0/kicks/main
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/right_click
#

# Kick type, and a random value from 1 to 5.
scoreboard players set #kick mgs.data 0
execute store result score #kick mgs.data run data get storage mgs:gun all.stats.kick
execute store result score #random mgs.data run random value 1..5

# In a vehicle, /rotate instead of /tp, which would dismount.
scoreboard players set #has_vehicle mgs.data 0
execute on vehicle run scoreboard players set #has_vehicle mgs.data 1

# Deadshot Daiquiri (zombies): the 65% kick tables.
execute if score @s mgs.special.deadshot matches 1 run return run function mgs:v5.1.0/kicks/apply_ds

function mgs:v5.1.0/kicks/apply

