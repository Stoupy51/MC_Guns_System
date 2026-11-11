
#> mgs:v5.4.2/zombies/rise_dust_tick
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/game_tick [ at @s ]
#

function mgs:v5.4.2/zombies/rise_dust_particles with entity @s data
scoreboard players remove @s mgs.zb.rise_tick 1
execute if score @s mgs.zb.rise_tick matches ..0 run kill @s

