
#> mgs:v5.0.0/multiplayer/class/support
#
# @within	???
#

# Apply class: Support - Suppressive heavy
clear @s
# Primary weapon → hotbar.0
loot replace entity @s hotbar.0 loot mgs:i/m249

# Secondary weapon → hotbar.1
loot replace entity @s hotbar.1 loot mgs:i/glock17

# Equipment → hotbar.8, hotbar.7, ...
loot replace entity @s hotbar.8 loot mgs:i/smoke_grenade
item modify entity @s hotbar.8 {"function":"minecraft:set_count","count":2,"add":false}

# Magazines → inventory.0, inventory.1, ...
loot replace entity @s inventory.0 loot mgs:i/m249_mag
loot replace entity @s inventory.1 loot mgs:i/m249_mag
loot replace entity @s inventory.2 loot mgs:i/m249_mag
loot replace entity @s inventory.3 loot mgs:i/glock17_mag
loot replace entity @s inventory.4 loot mgs:i/glock17_mag

