
#> mgs:v5.1.0/progression/tick_player
#
# @executed	as @a
#
# @within	mgs:v5.1.0/tick [ as @a ]
#

execute unless score @s mgs.mp.xp_level matches 1.. run function mgs:v5.1.0/progression/mp/init
execute unless score @s mgs.zb.xp_level matches 1.. run function mgs:v5.1.0/progression/zb/init

# Zombies owns the bar while its game is running; multiplayer and the lobby show the multiplayer level.
execute if score @s mgs.zb.in_game matches 1 run return run function mgs:v5.1.0/progression/zb/refresh_bar
function mgs:v5.1.0/progression/mp/refresh_bar

