
#> mgs:v5.0.0/ammo/apply_quick_reload
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/reload
#

# Calculate reduced cooldown: cooldown = cooldown * (100 - quick_reload%) / 100
scoreboard players set #100 mgs.data 100
scoreboard players operation #reduction mgs.data = #100 mgs.data
scoreboard players operation #reduction mgs.data -= @s mgs.special.quick_reload
scoreboard players operation @s mgs.cooldown *= #reduction mgs.data
scoreboard players operation @s mgs.cooldown /= #100 mgs.data

# Ensure minimum cooldown of 1 tick
execute if score @s mgs.cooldown matches ..0 run scoreboard players set @s mgs.cooldown 1

