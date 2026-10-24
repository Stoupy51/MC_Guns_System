
#> mgs:v5.2.0/players/mp_to_blue
#
# @within	string in mgs:v5.2.0/players/row_multiplayer
#

execute if score @s mgs.mi.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.leave_your_current_game_first","fallback":"Leave your current game first!","color":"red"}]
execute if score @s mgs.zb.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.leave_your_current_game_first","fallback":"Leave your current game first!","color":"red"}]
execute if score @s mgs.mp.in_game matches 0 if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.2.0/multiplayer/join_game
execute if score @s mgs.mp.in_game matches 0 if data storage mgs:multiplayer game{state:"preparing"} run function mgs:v5.2.0/multiplayer/join_game
scoreboard players set @s mgs.mp.in_game 1
scoreboard players set @s mgs.mp.team 2
team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.assigned_to","fallback":"Assigned to ","color":"white"},{"translate":"mgs.blue_team","fallback":"Blue Team","color":"blue","bold":true}]

