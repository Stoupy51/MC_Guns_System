
#> mgs:v5.0.0/switch/apply_quick_swap
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/on_weapon_switch
#

# Calculate reduced cooldown: cooldown = cooldown * (100 - quick_swap%) / 100
scoreboard players operation #reduction mgs.data = #100 mgs.data
scoreboard players operation #reduction mgs.data -= @s mgs.special.quick_swap
scoreboard players operation #cooldown mgs.data *= #reduction mgs.data
scoreboard players operation #cooldown mgs.data /= #100 mgs.data

# Ensure minimum cooldown of 1 tick
execute if score #cooldown mgs.data matches ..0 run scoreboard players set #cooldown mgs.data 1

