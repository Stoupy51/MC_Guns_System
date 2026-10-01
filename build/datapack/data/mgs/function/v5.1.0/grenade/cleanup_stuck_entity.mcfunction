
#> mgs:v5.1.0/grenade/cleanup_stuck_entity
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/delete
#

scoreboard players operation #my_stuck mgs.data = @s mgs.stuck_id

execute as @e[scores={mgs.stuck_id=1..}] if score @s mgs.stuck_id = #my_stuck mgs.data unless entity @s[tag=mgs.grenade] run scoreboard players reset @s mgs.stuck_id

