
#> mgs:v5.1.0/players/zb_join
#
# @within	mgs:v5.1.0/players/row_zombies
#			mgs:v5.1.0/dialogs/zombies/setup {"label": ["", "\ud83e\uddec ", {"translate": "mgs.variant"}], "tooltip": {"translate": "mgs.choose_the_zombies_experience"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/zombies/setup/variant"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/stop"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_zombies"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.all_players_join", "color": "green"}], "tooltip": {"translate": "mgs.add_every_online_player_to_the_zombies_game"}, "action": {"type": "run_command", "command": "/execute as @a run function mgs:v5.1.0/players/zb_join"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_zombies_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/join_game"}}], "columns": 2, "exit_action": {"label": ["", "\u25c0 ", {"translate": "mgs.back", "color": "gray"}], "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

execute if score @s mgs.zb.in_game matches 0 if data storage mgs:zombies game{state:"active"} run function mgs:v5.1.0/zombies/join_game
execute if score @s mgs.zb.in_game matches 0 if data storage mgs:zombies game{state:"preparing"} run function mgs:v5.1.0/zombies/join_game
scoreboard players set @s mgs.zb.in_game 1
execute if data storage mgs:zombies game{state:"active"} run team join mgs.zombies @s
execute if data storage mgs:zombies game{state:"preparing"} run team join mgs.zombies @s
tellraw @s ["",{"translate":"mgs.joined_the","color":"white"},{"translate":"mgs.zombies_game","color":"dark_green","bold":true}]

