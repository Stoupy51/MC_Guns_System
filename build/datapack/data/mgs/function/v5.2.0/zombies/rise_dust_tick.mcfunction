
#> mgs:v5.2.0/zombies/rise_dust_tick
#
# @executed	at @s
#
# @within	mgs:v5.2.0/zombies/game_tick [ at @s ]
#

function mgs:v5.2.0/zombies/rise_dust_particles with entity @s data
scoreboard players remove @s mgs.zb.rise_tick 1
execute if score @s mgs.zb.rise_tick matches ..0 run kill @s

