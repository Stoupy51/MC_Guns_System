
#> mgs:v5.1.0/players/mp_remove
#
# @within	mgs:v5.1.0/players/multiplayer_menu as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_to_blue"}},{label:{translate:"mgs.remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_multiplayer"}}}
#

scoreboard players set @s mgs.mp.team 0
scoreboard players set @s mgs.mp.in_game 0
team leave @s
execute if data storage mgs:multiplayer game{state:"active"} run gamemode spectator @s
tellraw @s [{"translate":"mgs.removed_from_the_game","color":"gray"}]

