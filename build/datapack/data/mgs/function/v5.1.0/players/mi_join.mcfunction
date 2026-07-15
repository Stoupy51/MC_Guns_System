
#> mgs:v5.1.0/players/mi_join
#
# @within	mgs:v5.1.0/players/missions_menu as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mi_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_missions"}}}
#

execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"active"} run function mgs:v5.1.0/missions/join_game
execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"preparing"} run function mgs:v5.1.0/missions/join_game
scoreboard players set @s mgs.mi.in_game 1
scoreboard players set @s mgs.mp.team 1
execute if data storage mgs:missions game{state:"active"} run team join mgs.blue @s
execute if data storage mgs:missions game{state:"preparing"} run team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.joined_the","color":"white"},{"translate":"mgs.mission","color":"aqua","bold":true}]

