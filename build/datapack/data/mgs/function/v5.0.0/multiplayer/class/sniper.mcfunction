
#> mgs:v5.0.0/multiplayer/class/sniper
#
# @within	???
#

# Apply class: Sniper - Long-range precision
clear @s
# Primary weapon → hotbar.0
loot replace entity @s hotbar.0 loot mgs:i/m24

# Secondary weapon → hotbar.1
loot replace entity @s hotbar.1 loot mgs:i/deagle

# Equipment → hotbar.8, hotbar.7, ...
loot replace entity @s hotbar.8 loot mgs:i/flash_grenade

# Magazines → inventory.0, inventory.1, ...
loot replace entity @s inventory.0 loot mgs:i/m24_bullet
scoreboard players set #bullets mgs.data 10
item modify entity @s inventory.0 mgs:v5.0.0/set_consumable_count
loot replace entity @s inventory.1 loot mgs:i/deagle_mag
loot replace entity @s inventory.2 loot mgs:i/deagle_mag

