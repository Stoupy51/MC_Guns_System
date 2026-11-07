
#> mgs:v5.4.0/kicks/main
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/player/right_click
#

scoreboard players set #kick mgs.data 0
execute store result score #kick mgs.data run data get storage mgs:gun all.stats.kick
execute if score #kick mgs.data matches ..-1 run scoreboard players set #kick mgs.data 0
execute if score #kick mgs.data matches 6.. run scoreboard players set #kick mgs.data 5
scoreboard players operation @s mgs.kick = #kick mgs.data
execute store result score @s mgs.kick_dir run random value 1..5

