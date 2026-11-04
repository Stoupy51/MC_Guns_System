
#> mgs:v5.3.0/zombies/pap/anim/step_timeslip
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/game_tick [ at @s ]
#

execute if score @s mgs.pap_anim matches 206.. run function mgs:v5.3.0/zombies/pap/anim/step
execute if score @s mgs.pap_anim matches 206.. run function mgs:v5.3.0/zombies/pap/anim/step

