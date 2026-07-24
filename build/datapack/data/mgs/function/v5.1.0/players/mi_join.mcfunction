
#> mgs:v5.1.0/players/mi_join
#
# @executed	as the player & at current position
#
# @within	string in mgs:v5.1.0/players/row_missions
#			dialog mgs:v5.1.0/missions/setup
#

execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"active"} run function mgs:v5.1.0/missions/join_game
execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"preparing"} run function mgs:v5.1.0/missions/join_game
scoreboard players set @s mgs.mi.in_game 1
scoreboard players set @s mgs.mp.team 1
execute if data storage mgs:missions game{state:"active"} run team join mgs.blue @s
execute if data storage mgs:missions game{state:"preparing"} run team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.joined_the","color":"white"},{"translate":"mgs.mission","color":"aqua","bold":true}]

