
#> mgs:v5.0.0/zombies/on_zombie_dying
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/death_watch_tick [ at @s ]
#

# Guard: only process round zombies.
execute unless entity @s[tag=mgs.zombie_round] run return 0

# Kill the attached death-watch marker while still mounted to avoid orphan buildup.
kill @n[type=minecraft:marker,tag=mgs.death_watch,distance=..1]

# Check if a power-up should drop at this zombie's position.
function mgs:v5.0.0/zombies/powerups/check_drop

# Remove zombie before vanilla death event 60 can fire.
tp @s ~ -10000 ~

