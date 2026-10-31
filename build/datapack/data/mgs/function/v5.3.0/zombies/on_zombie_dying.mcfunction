
#> mgs:v5.3.0/zombies/on_zombie_dying
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/death_watch_tick [ at @s ]
#

execute if entity @s[tag=mgs.zb_escorted] at @s run function mgs:v5.3.0/zombies/escort/on_escorted_killed


execute unless entity @s[tag=mgs.zombie_round] run return 0

# Kill the death-watch marker while still mounted, so none are orphaned.
kill @n[type=minecraft:marker,tag=mgs.death_watch,distance=..1]

# Riders fight on as enemies of their own; the teleport below would take them along.
execute on passengers run ride @s dismount

# Special rounds never roll the drop table: they only drop the Max Ammo of their last enemy.
execute unless score #zb_special_round mgs.data matches 1 run function mgs:v5.3.0/zombies/powerups/check_drop

# Armed enemies have a 5% chance to drop a Max Ammo, whatever killed them, on top of the usual roll.
execute if entity @s[tag=mgs.armed] if predicate {type:"minecraft:random_chance",chance:0.05} run function mgs:v5.3.0/zombies/max_ammo_at_self

# "Was this the last one" needs an exact count.
execute if score #zb_special_round mgs.data matches 1 run function mgs:v5.3.0/zombies/special_death

# Removed before vanilla death event 60 fires.
tp @s ~ -10000 ~

