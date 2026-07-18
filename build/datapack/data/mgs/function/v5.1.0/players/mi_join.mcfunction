
#> mgs:v5.1.0/players/mi_join
#
# @within	mgs:v5.1.0/players/row_missions
#			mgs:v5.1.0/dialogs/missions/setup {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_missions"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.all_players_join", "color": "green"}], "tooltip": {"translate": "mgs.add_every_online_player_to_the_mission"}, "action": {"type": "run_command", "command": "/execute as @a run function mgs:v5.1.0/players/mi_join"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_mission_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/join_game"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"active"} run function mgs:v5.1.0/missions/join_game
execute if score @s mgs.mi.in_game matches 0 if data storage mgs:missions game{state:"preparing"} run function mgs:v5.1.0/missions/join_game
scoreboard players set @s mgs.mi.in_game 1
scoreboard players set @s mgs.mp.team 1
execute if data storage mgs:missions game{state:"active"} run team join mgs.blue @s
execute if data storage mgs:missions game{state:"preparing"} run team join mgs.blue @s
tellraw @s ["",{"translate":"mgs.joined_the","color":"white"},{"translate":"mgs.mission","color":"aqua","bold":true}]

