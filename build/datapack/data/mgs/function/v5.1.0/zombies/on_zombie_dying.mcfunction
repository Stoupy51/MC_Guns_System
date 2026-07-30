
#> mgs:v5.1.0/zombies/on_zombie_dying
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/death_watch_tick [ at @s ]
#

# Escorted zombie died: remove its escort trader immediately (escort.py)
execute if entity @s[tag=mgs.zb_escorted] at @s run function mgs:v5.1.0/zombies/escort/on_escorted_killed

# Guard: only process round zombies.
execute unless entity @s[tag=mgs.zombie_round] run return 0

# Kill the attached death-watch marker while still mounted to avoid orphan buildup.
kill @n[type=minecraft:marker,tag=mgs.death_watch,distance=..1]

# Check if a power-up should drop at this zombie's position. Dogs never roll the random table — a
# dog round's only drop is the guaranteed Max Ammo from the last hound.
execute unless entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/powerups/check_drop

# Dogs: handle the death separately, since "was this the last one" needs an exact count.
execute if entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/dog_death

# Remove zombie before vanilla death event 60 can fire.
tp @s ~ -10000 ~

