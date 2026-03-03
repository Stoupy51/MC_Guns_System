
#> mgs:v5.0.0/multiplayer/class/rifleman
#
# @within	???
#

# Apply class: Rifleman - Accurate mid-range
clear @s
# Primary weapon → hotbar.0
loot replace entity @s hotbar.0 loot mgs:i/m16a4

# Secondary weapon → hotbar.1
loot replace entity @s hotbar.1 loot mgs:i/m9

# Equipment → hotbar.8, hotbar.7, ...
loot replace entity @s hotbar.8 loot mgs:i/flash_grenade
loot replace entity @s hotbar.7 loot mgs:i/smoke_grenade

# Magazines → inventory.0, inventory.1, ...
loot replace entity @s inventory.0 loot mgs:i/m16a4_mag
loot replace entity @s inventory.1 loot mgs:i/m16a4_mag
loot replace entity @s inventory.2 loot mgs:i/m16a4_mag
loot replace entity @s inventory.3 loot mgs:i/m9_mag
loot replace entity @s inventory.4 loot mgs:i/m9_mag

