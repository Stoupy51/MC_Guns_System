
#> mgs:v5.0.0/kicks/main
#
# @within	mgs:v5.0.0/player/right_click
#

# Extract kick type & pick random value between 1 and 5
scoreboard players set #kick mgs.data 0
execute store result score #kick mgs.data run data get storage mgs:gun all.stats.kick
execute store result score #random mgs.data run random value 1..5

# Check if player is riding a vehicle - if so, use /rotate instead of /tp to avoid dismounting
scoreboard players set #has_vehicle mgs.data 0
execute on vehicle run scoreboard players set #has_vehicle mgs.data 1

# Switch case
execute if score #kick mgs.data matches ..0 run function mgs:v5.0.0/kicks/type_0
execute if score #kick mgs.data matches 1 run function mgs:v5.0.0/kicks/type_1
execute if score #kick mgs.data matches 2 run function mgs:v5.0.0/kicks/type_2
execute if score #kick mgs.data matches 3 run function mgs:v5.0.0/kicks/type_3
execute if score #kick mgs.data matches 4 run function mgs:v5.0.0/kicks/type_4
execute if score #kick mgs.data matches 5.. run function mgs:v5.0.0/kicks/type_5

