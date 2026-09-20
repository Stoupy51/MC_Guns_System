
#> mgs:v5.1.0/zoom/fx_enter
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/set
#

# @s = a player who just entered aim-down-sights
scoreboard players set #scope_level mgs.data 2
execute store result score #scope_level mgs.data run data get storage mgs:gun all.stats.scope_level
execute unless score #scope_level mgs.data matches 3..4 run scoreboard players set #scope_level mgs.data 2
function mgs:v5.1.0/zoom/fx_clear
execute if score #scope_level mgs.data matches 2 run function mgs:v5.1.0/zoom/fx_enter_2
execute if score #scope_level mgs.data matches 3 run function mgs:v5.1.0/zoom/fx_enter_3
execute if score #scope_level mgs.data matches 4 run function mgs:v5.1.0/zoom/fx_enter_4

