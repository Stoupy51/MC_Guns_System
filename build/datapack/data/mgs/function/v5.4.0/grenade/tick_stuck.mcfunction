
#> mgs:v5.4.0/grenade/tick_stuck
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/grenade/tick
#

execute if entity @s[tag=mgs.stuck_to_entity] run function mgs:v5.4.0/grenade/follow_entity

scoreboard players operation @s mgs.data -= #tick_delta mgs.data

# Blinking before the blast.
particle small_flame ~ ~0.3 ~ 0 0 0 0 1 force @a[distance=..32]

execute if score @s mgs.data matches ..0 run function mgs:v5.4.0/grenade/detonate

