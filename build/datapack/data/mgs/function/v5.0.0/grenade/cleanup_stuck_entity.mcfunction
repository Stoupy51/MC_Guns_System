
#> mgs:v5.0.0/grenade/cleanup_stuck_entity
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.0.0/grenade/delete
#

# Read my stuck ID
scoreboard players operation #my_stuck mgs.data = @s mgs.stuck_id

# Find the paired entity and reset its stuck_id
execute as @e[scores={mgs.stuck_id=1..}] if score @s mgs.stuck_id = #my_stuck mgs.data unless entity @s[tag=mgs.grenade] run scoreboard players reset @s mgs.stuck_id

