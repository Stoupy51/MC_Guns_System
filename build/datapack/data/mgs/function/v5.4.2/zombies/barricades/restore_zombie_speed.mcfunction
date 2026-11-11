
#> mgs:v5.4.2/zombies/barricades/restore_zombie_speed
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/game_tick [ as @e[tag=...] ]
#

attribute @s minecraft:movement_speed modifier remove mgs:freeze
tag @s remove mgs.barricade_frozen

