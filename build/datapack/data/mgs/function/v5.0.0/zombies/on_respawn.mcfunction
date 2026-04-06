
#> mgs:v5.0.0/zombies/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Reset death counter
scoreboard players set @s mgs.mp.death_count 0

# Increment down count
scoreboard players add @s mgs.zb.downs 1

# Enter downed state (revive system)
function mgs:v5.0.0/zombies/revive/on_down

