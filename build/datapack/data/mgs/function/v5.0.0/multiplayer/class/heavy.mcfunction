
#> mgs:v5.0.0/multiplayer/class/heavy
#
# @executed	as @a & at @s
#
# @within	mgs:v5.0.0/multiplayer/apply_class
#

# Apply class: Heavy - Armored suppressor
clear @s
# Primary weapon → hotbar.0
loot replace entity @s hotbar.0 loot mgs:i/rpk

# Secondary weapon → hotbar.1
loot replace entity @s hotbar.1 loot mgs:i/makarov

# Equipment → hotbar.8, hotbar.7, ...
loot replace entity @s hotbar.8 loot mgs:i/frag_grenade
item modify entity @s hotbar.8 {"function":"minecraft:set_count","count":2,"add":false}

# Magazines → inventory.0, inventory.1, ...
loot replace entity @s inventory.0 loot mgs:i/rpk_mag
loot replace entity @s inventory.1 loot mgs:i/rpk_mag
loot replace entity @s inventory.2 loot mgs:i/rpk_mag
loot replace entity @s inventory.3 loot mgs:i/makarov_mag
loot replace entity @s inventory.4 loot mgs:i/makarov_mag

