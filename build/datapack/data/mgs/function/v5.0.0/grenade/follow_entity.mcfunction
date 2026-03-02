
#> mgs:v5.0.0/grenade/follow_entity
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/tick_stuck
#

# Tag myself for the teleportation
tag @s add mgs.tp_me

# Read my stuck ID
scoreboard players operation #my_stuck mgs.data = @s mgs.stuck_id

# Find the entity with matching stuck_id (not a grenade) and teleport me to it
execute as @e[scores={mgs.stuck_id=1..}] if score @s mgs.stuck_id = #my_stuck mgs.data unless entity @s[tag=mgs.grenade] at @s run tp @n[tag=mgs.tp_me] ~ ~ ~

# Remove temp tag
tag @s remove mgs.tp_me

