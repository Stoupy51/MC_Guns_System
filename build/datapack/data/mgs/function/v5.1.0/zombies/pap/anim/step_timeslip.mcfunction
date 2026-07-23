
#> mgs:v5.1.0/zombies/pap/anim/step_timeslip
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

execute if score @s mgs.pap_anim matches 1.. run function mgs:v5.1.0/zombies/pap/anim/step
execute if score @s mgs.pap_anim matches 1.. run function mgs:v5.1.0/zombies/pap/anim/step

