
#> mgs:v5.0.0/zombies/perks/check_coward
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/ability_tick [ at @s ]
#

# Check health: 10 HP = 50% of default 20 HP max
execute store result score #hp mgs.data run data get entity @s Health 1
execute if score #hp mgs.data matches ..10 run function mgs:v5.0.0/zombies/perks/trigger_coward

