
#> mgs:v5.3.0/zombies/barricades/restore_zombie_speed
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/game_tick [ as @e[tag=...] ]
#

attribute @s minecraft:movement_speed modifier remove mgs:freeze
tag @s remove mgs.barricade_frozen

