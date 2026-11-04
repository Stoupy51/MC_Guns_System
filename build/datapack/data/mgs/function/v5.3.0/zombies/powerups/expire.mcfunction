
#> mgs:v5.3.0/zombies/powerups/expire
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/powerups/entity_tick
#

kill @n[type=minecraft:text_display,tag=mgs.pu_text,distance=..3]
kill @s
scoreboard players remove #pu_active mgs.data 1

