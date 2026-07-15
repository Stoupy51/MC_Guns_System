
#> mgs:v5.1.0/players/mp_to_red
#
# @within	mgs:v5.1.0/players/multiplayer_menu as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_to_blue"}},{label:{translate:"mgs.remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_multiplayer"}}}
#

execute if score @s mgs.mp.in_game matches 0 if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.1.0/multiplayer/join_game
execute if score @s mgs.mp.in_game matches 0 if data storage mgs:multiplayer game{state:"preparing"} run function mgs:v5.1.0/multiplayer/join_game
scoreboard players set @s mgs.mp.in_game 1
scoreboard players set @s mgs.mp.team 1
execute if data storage mgs:multiplayer game{state:"active"} run team join mgs.red @s
execute if data storage mgs:multiplayer game{state:"preparing"} run team join mgs.red @s
tellraw @s ["",{"translate":"mgs.assigned_to","color":"white"},{"translate":"mgs.red_team","color":"red","bold":true}]

