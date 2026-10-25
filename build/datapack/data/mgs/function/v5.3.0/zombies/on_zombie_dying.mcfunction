
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

# Dogs never roll the drop table: a dog round only drops the Max Ammo of its last hound.
execute unless entity @s[tag=mgs.zb_dog] run function mgs:v5.3.0/zombies/powerups/check_drop

# Armed zombies have a 5% chance to drop a Max Ammo, whatever killed them, on top of the usual roll.
execute if entity @s[tag=mgs.zb_armed] if predicate {type:"minecraft:random_chance",chance:0.05} run function mgs:v5.3.0/zombies/max_ammo_at_self

# Dogs: "was this the last one" needs an exact count.
execute if entity @s[tag=mgs.zb_dog] run function mgs:v5.3.0/zombies/dog_death

# Removed before vanilla death event 60 fires.
tp @s ~ -10000 ~

