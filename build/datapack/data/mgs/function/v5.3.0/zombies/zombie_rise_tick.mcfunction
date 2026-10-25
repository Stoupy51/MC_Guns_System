
#> mgs:v5.3.0/zombies/zombie_rise_tick
#
# @executed	at @s
#
# @within	mgs:v5.3.0/zombies/game_tick [ at @s ]
#

execute store result storage mgs:temp _rise.dy double 0.001 run scoreboard players get @s mgs.zb.rise_step
function mgs:v5.3.0/zombies/zombie_rise_move with storage mgs:temp _rise

scoreboard players remove @s mgs.zb.rise_tick 1
execute if score @s mgs.zb.rise_tick matches ..0 run function mgs:v5.3.0/zombies/zombie_finish_rise

