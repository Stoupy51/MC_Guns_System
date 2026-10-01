
#> mgs:v5.1.0/multiplayer/get_username
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/save [ at @s ]
#

# Run as the item_display, at the player.
tag @s add mgs.username_getter_entity

# As the player, so the loot table's `this` is them and the head carries their profile.
execute at @s as @n[tag=mgs.username_getter] run loot replace entity @n[tag=mgs.username_getter_entity] contents loot mgs:get_username

data modify storage mgs:temp _new_loadout.owner_name set from entity @s item.components."minecraft:profile".name

# No profile captured.
execute unless data storage mgs:temp _new_loadout.owner_name run data modify storage mgs:temp _new_loadout.owner_name set value ""

kill @s

