
#> mgs:v5.0.0/zombies/pap/anim_retreat_step
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

scoreboard players remove @s mgs.pap_anim 1
particle smoke ~ ~0.5 ~ 0.2 0.2 0.2 0.05 2 force

