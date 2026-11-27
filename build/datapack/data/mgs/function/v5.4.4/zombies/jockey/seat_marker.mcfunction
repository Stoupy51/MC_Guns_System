
#> mgs:v5.4.4/zombies/jockey/seat_marker
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/zombies/mob/setup
#

execute on passengers if entity @s[type=minecraft:marker] run function mgs:v5.4.4/zombies/jockey/reseat_marker

