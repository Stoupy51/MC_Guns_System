
#> mgs:v5.0.0/multiplayer/get_username
#
# @executed	at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save [ at @s ]
#

# @s = item_display entity spawned at the player's position
# Tag this entity so we can reference it from within the execute-as subcommand
tag @s add mgs.username_getter_entity

# Execute AS the calling player (tagged), run loot replace targeting THIS entity
# The loot table fills a player_head using "this" entity = the executing player
execute at @s as @n[tag=mgs.username_getter] run loot replace entity @n[tag=mgs.username_getter_entity] contents loot mgs:get_username

# Store the username from the player head profile component
data modify storage mgs:temp _new_loadout.owner_name set from entity @s item.components."minecraft:profile".name

# Fallback if profile was not captured
execute unless data storage mgs:temp _new_loadout.owner_name run data modify storage mgs:temp _new_loadout.owner_name set value ""

# Clean up: kill this entity
kill @s

