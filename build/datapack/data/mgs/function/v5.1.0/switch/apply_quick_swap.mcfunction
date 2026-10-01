
#> mgs:v5.1.0/switch/apply_quick_swap
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/on_weapon_switch
#

# cooldown x (100 - quick_swap) / 100
scoreboard players operation #reduction mgs.data = #100 mgs.data
scoreboard players operation #reduction mgs.data -= @s mgs.special.quick_swap
scoreboard players operation #cooldown mgs.data *= #reduction mgs.data
scoreboard players operation #cooldown mgs.data /= #100 mgs.data

# At least 1 tick.
execute if score #cooldown mgs.data matches ..0 run scoreboard players set #cooldown mgs.data 1

