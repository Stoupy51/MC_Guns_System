
#> mgs:v5.1.0/players/mp_to_blue
#
# @within	string in mgs:v5.1.0/players/row_multiplayer
#

execute if score @s mgs.mp.in_game matches 0 if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.1.0/multiplayer/join_game
execute if score @s mgs.mp.in_game matches 0 if data storage mgs:multiplayer game{state:"preparing"} run function mgs:v5.1.0/multiplayer/join_game
scoreboard players set @s mgs.mp.in_game 1
scoreboard players set @s mgs.mp.team 2
execute if data storage mgs:multiplayer game{state:"active"} run team join mgs.blue @s
execute if data storage mgs:multiplayer game{state:"preparing"} run team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.assigned_to","color":"white"},{"translate":"mgs.blue_team","color":"blue","bold":true}]

