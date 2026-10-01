
#> mgs:v5.1.0/grenade/follow_entity
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/tick_stuck
#

tag @s add mgs.tp_me

scoreboard players operation #my_stuck mgs.data = @s mgs.stuck_id

# The entity with the same stuck_id that is not a grenade.
execute as @e[scores={mgs.stuck_id=1..}] if score @s mgs.stuck_id = #my_stuck mgs.data unless entity @s[tag=mgs.grenade] at @s run tp @n[tag=mgs.tp_me] ~ ~ ~

tag @s remove mgs.tp_me

