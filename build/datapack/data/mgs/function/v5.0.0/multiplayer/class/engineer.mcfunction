
#> mgs:v5.0.0/multiplayer/class/engineer
#
# @within	???
#

# Apply class: Engineer - Objective / demolitions
clear @s
# Primary weapon → hotbar.0
loot replace entity @s hotbar.0 loot mgs:i/mp5

# Secondary weapon → hotbar.1
loot replace entity @s hotbar.1 loot mgs:i/makarov

# Equipment → hotbar.8, hotbar.7, ...
loot replace entity @s hotbar.8 loot mgs:i/semtex
item modify entity @s hotbar.8 {"function":"minecraft:set_count","count":2,"add":false}
loot replace entity @s hotbar.7 loot mgs:i/smoke_grenade

# Magazines → inventory.0, inventory.1, ...
loot replace entity @s inventory.0 loot mgs:i/mp5_mag
loot replace entity @s inventory.1 loot mgs:i/mp5_mag
loot replace entity @s inventory.2 loot mgs:i/mp5_mag
loot replace entity @s inventory.3 loot mgs:i/makarov_mag
loot replace entity @s inventory.4 loot mgs:i/makarov_mag

