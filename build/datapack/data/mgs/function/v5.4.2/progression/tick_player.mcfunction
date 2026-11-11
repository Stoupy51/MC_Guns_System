
#> mgs:v5.4.2/progression/tick_player
#
# @executed	as @a
#
# @within	mgs:v5.4.2/tick [ as @a ]
#			mgs:v5.4.2/dialog/close_then
#

execute if score @s mgs.mi.in_game matches 1 if data storage mgs:missions game{state:"active"} run function mgs:v5.4.2/stats/mi/second
execute if score @s mgs.mp.in_game matches 1 if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.4.2/stats/mp/second
execute if score @s mgs.zb.in_game matches 1 if data storage mgs:zombies game{state:"active"} run function mgs:v5.4.2/stats/zb/second
execute unless score @s mgs.st.login matches 0 run function mgs:v5.4.2/stats/login
execute unless score @s mgs.adv.caught matches 1 run function mgs:v5.4.2/progression/adv/catch_up

execute unless score @s mgs.mp.xp_level matches 1.. run function mgs:v5.4.2/progression/mp/init
execute unless score @s mgs.zb.xp_level matches 1.. run function mgs:v5.4.2/progression/zb/init

# Zombies owns the bar while its game runs; the multiplayer level shows only to its players, so a host datapack can keep using the vanilla XP.
execute if score @s mgs.zb.in_game matches 1 run return run function mgs:v5.4.2/progression/zb/refresh_bar
execute if score @s mgs.mp.in_game matches 1 run function mgs:v5.4.2/progression/mp/refresh_bar

