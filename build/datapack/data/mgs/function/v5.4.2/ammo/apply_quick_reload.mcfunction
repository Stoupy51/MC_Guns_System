
#> mgs:v5.4.2/ammo/apply_quick_reload
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/ammo/reload
#

# cooldown x (100 - quick_reload) / 100
scoreboard players operation #reduction mgs.data = #100 mgs.data
scoreboard players operation #reduction mgs.data -= @s mgs.special.quick_reload
scoreboard players operation @s mgs.cooldown *= #reduction mgs.data
scoreboard players operation @s mgs.cooldown /= #100 mgs.data

# At least 1 tick.
execute if score @s mgs.cooldown matches ..0 run scoreboard players set @s mgs.cooldown 1

