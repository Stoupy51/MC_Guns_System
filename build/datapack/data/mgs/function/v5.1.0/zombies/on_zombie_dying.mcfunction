
#> mgs:v5.1.0/zombies/on_zombie_dying
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/death_watch_tick [ at @s ]
#

execute if entity @s[tag=mgs.zb_escorted] at @s run function mgs:v5.1.0/zombies/escort/on_escorted_killed


execute unless entity @s[tag=mgs.zombie_round] run return 0

# Kill the death-watch marker while still mounted, so none are orphaned.
kill @n[type=minecraft:marker,tag=mgs.death_watch,distance=..1]

# Dogs never roll the drop table: a dog round only drops the Max Ammo of its last hound.
execute unless entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/powerups/check_drop

# Dogs: "was this the last one" needs an exact count.
execute if entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/dog_death

# Removed before vanilla death event 60 fires.
tp @s ~ -10000 ~

