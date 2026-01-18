
#> mgs:v5.0.0/switch/main
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Set weapon id if not done yet
execute if data storage mgs:gun all.stats unless data storage mgs:gun all.stats.weapon_id run function mgs:v5.0.0/switch/set_weapon_id

# If last_selected is different from this one, set cooldown
scoreboard players set #current_id mgs.data 0
execute store result score #current_id mgs.data run data get storage mgs:gun all.stats.weapon_id
execute unless score @s mgs.last_selected = #current_id mgs.data run function mgs:v5.0.0/switch/on_weapon_switch

# Update last selected
scoreboard players operation @s mgs.last_selected = #current_id mgs.data

