
#> mgs:v5.0.0/zombies/powerups/expire
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/entity_tick
#

kill @e[tag=mgs.pu_text,distance=..3]
kill @s

