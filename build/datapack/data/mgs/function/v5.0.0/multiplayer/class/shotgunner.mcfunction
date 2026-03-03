
#> mgs:v5.0.0/multiplayer/class/shotgunner
#
# @within	???
#

# Apply class: Shotgunner - Breaching / CQB
clear @s
# Primary weapon → hotbar.0
loot replace entity @s hotbar.0 loot mgs:i/spas12

# Secondary weapon → hotbar.1
loot replace entity @s hotbar.1 loot mgs:i/m9

# Equipment → hotbar.8, hotbar.7, ...
loot replace entity @s hotbar.8 loot mgs:i/semtex
item modify entity @s hotbar.8 {"function":"minecraft:set_count","count":2,"add":false}

# Magazines → inventory.0, inventory.1, ...
loot replace entity @s inventory.0 loot mgs:i/spas12_shell
scoreboard players set #bullets mgs.data 16
item modify entity @s inventory.0 mgs:v5.0.0/set_consumable_count
loot replace entity @s inventory.1 loot mgs:i/m9_mag
loot replace entity @s inventory.2 loot mgs:i/m9_mag

