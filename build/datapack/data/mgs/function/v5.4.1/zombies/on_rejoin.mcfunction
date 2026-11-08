
#> mgs:v5.4.1/zombies/on_rejoin
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.1/player/tick
#			mgs:v5.4.1/dialog/close_then
#

scoreboard players set @s mgs.zb.rejoins 0
execute unless score @s mgs.zb.run matches 1.. run return 0

execute unless score @s mgs.zb.run = #zb_run mgs.data run return run function mgs:v5.4.1/zombies/clear_stale_player
execute if data storage mgs:zombies game{state:"lobby"} run return run function mgs:v5.4.1/zombies/clear_stale_player
execute if data storage mgs:zombies game{state:"active"} run function mgs:v5.4.1/zombies/rejoin

