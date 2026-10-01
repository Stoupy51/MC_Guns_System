
#> mgs:v5.1.0/zombies/perks/check_coward
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/ability_tick [ at @s ]
#

# 10 HP is half the default 20.
execute store result score #hp mgs.data run data get entity @s Health 1
execute if score #hp mgs.data matches ..10 run function mgs:v5.1.0/zombies/perks/trigger_coward

