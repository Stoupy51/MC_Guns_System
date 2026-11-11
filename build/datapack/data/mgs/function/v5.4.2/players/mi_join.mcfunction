
#> mgs:v5.4.2/players/mi_join
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/players/row_missions
#			dialog mgs:v5.4.2/missions/setup
#

execute if score @s mgs.mp.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.leave_your_current_game_first","fallback":"Leave your current game first!","color":"red"}]
execute if score @s mgs.zb.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.leave_your_current_game_first","fallback":"Leave your current game first!","color":"red"}]
execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"active"} run function mgs:v5.4.2/missions/join_game
execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"preparing"} run function mgs:v5.4.2/missions/join_game
scoreboard players set @s mgs.mi.in_game 1
scoreboard players set @s mgs.mp.team 1
team join mgs.missions @s
tellraw @s ["",{"translate":"mgs.joined_the","fallback":"Joined the ","color":"white"},{"translate":"mgs.mission","fallback":"Mission","color":"aqua","bold":true}]

