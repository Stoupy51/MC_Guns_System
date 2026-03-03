
#> mgs:v5.0.0/multiplayer/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Increment death stats
scoreboard players add @s mgs.mp.deaths 1

# Apply current class (auto-equip with loadout + bottom row selectors)
execute if score @s mgs.mp.class matches 1.. run function mgs:v5.0.0/multiplayer/apply_class

# If no class selected yet, give full selectors
execute unless score @s mgs.mp.class matches 1.. run function mgs:v5.0.0/multiplayer/give_class_selectors

