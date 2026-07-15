
#> mgs:v5.1.0/players/zb_remove
#
# @within	mgs:v5.1.0/players/zombies_menu as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/zb_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_zombies"}}}
#

scoreboard players set @s mgs.zb.in_game 0
team leave @s
execute if data storage mgs:zombies game{state:"active"} run gamemode spectator @s
tellraw @s [{"translate":"mgs.removed_from_the_zombies_game","color":"gray"}]

