
#> mgs:v5.4.2/stats/record_bullet
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/shoot
#

execute if score @s mgs.zb.in_game matches 1 if data storage mgs:zombies game{state:"active"} run scoreboard players add @s mgs.st.zb.shots 1
execute if score @s mgs.zb.in_game matches 1 if data storage mgs:zombies game{state:"active"} if score #bullet_hit mgs.data matches 1 run scoreboard players add @s mgs.st.zb.hits 1

execute if score @s mgs.mp.in_game matches 1 if data storage mgs:multiplayer game{state:"active"} run scoreboard players add @s mgs.st.mp.shots 1
execute if score @s mgs.mp.in_game matches 1 if data storage mgs:multiplayer game{state:"active"} if score #bullet_hit mgs.data matches 1 run scoreboard players add @s mgs.st.mp.hits 1

execute if score @s mgs.mi.in_game matches 1 if data storage mgs:missions game{state:"active"} run scoreboard players add @s mgs.st.mi.shots 1
execute if score @s mgs.mi.in_game matches 1 if data storage mgs:missions game{state:"active"} if score #bullet_hit mgs.data matches 1 run scoreboard players add @s mgs.st.mi.hits 1

