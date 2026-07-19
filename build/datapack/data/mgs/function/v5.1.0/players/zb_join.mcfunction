
#> mgs:v5.1.0/players/zb_join
#
# @within	mgs:v5.1.0/players/row_zombies
#

execute if score @s mgs.zb.in_game matches 0 if data storage mgs:zombies game{state:"active"} run function mgs:v5.1.0/zombies/join_game
execute if score @s mgs.zb.in_game matches 0 if data storage mgs:zombies game{state:"preparing"} run function mgs:v5.1.0/zombies/join_game
scoreboard players set @s mgs.zb.in_game 1
execute if data storage mgs:zombies game{state:"active"} run team join mgs.zombies @s
execute if data storage mgs:zombies game{state:"preparing"} run team join mgs.zombies @s
tellraw @s ["",{"translate":"mgs.joined_the","color":"white"},{"translate":"mgs.zombies_game","color":"dark_green","bold":true}]

