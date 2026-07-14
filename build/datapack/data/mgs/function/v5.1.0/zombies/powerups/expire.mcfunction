
#> mgs:v5.1.0/zombies/powerups/expire
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.1.0/zombies/powerups/entity_tick
#

kill @n[tag=mgs.pu_text,distance=..3]
kill @s
scoreboard players remove #pu_active mgs.data 1

