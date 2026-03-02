
#> mgs:v5.0.0/grenade/summon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/grenade/summon_loop
#

# Get accuracy value and apply spread
function mgs:v5.0.0/raycast/accuracy/get_value

# Summon the grenade entity at the player's eye position
execute anchored eyes positioned ^ ^ ^0.5 summon item_display run function mgs:v5.0.0/grenade/init

# Increment grenade counter
scoreboard players add #grenade_count mgs.data 1

