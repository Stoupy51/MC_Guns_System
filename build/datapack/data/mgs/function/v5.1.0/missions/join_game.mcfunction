
#> mgs:v5.1.0/missions/join_game
#
# @within	mgs:v5.1.0/players/mi_join
#			mgs:v5.1.0/dialogs/missions/setup {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_mission"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_missions"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_mission_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/missions/join_game"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_game_modes_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config/modes"}}}
#

# Require an active game
execute unless data storage mgs:missions game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_mission_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.mi.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_mission","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.mi.in_game 1
scoreboard players set @s mgs.mp.team 1
team join mgs.blue @s
scoreboard players set @s mgs.mi.kills 0
scoreboard players set @s mgs.mi.deaths 0
scoreboard players set @s mgs.mp.death_count 0
scoreboard players set @s mgs.mp.spectate_timer 0

# Setup player
gamemode adventure @s

# Reset stamina so the stamina system re-inits this player at full (it owns the hunger bar)
scoreboard players set @s mgs.stam_seen 0

# Enable class menu and show class selection
tag @s add mgs.give_class_menu
function mgs:v5.1.0/multiplayer/select_class

# Apply class if already chosen
execute unless score @s mgs.mp.class matches 0 run function mgs:v5.1.0/multiplayer/apply_class

item replace entity @s hotbar.3 with compass[custom_data={mgs:{compass:true}}]

# Teleport to spawn
function mgs:v5.1.0/missions/respawn_tp

# Call map join script (executed as the joining player)
function mgs:v5.1.0/shared/maps/call_join_script_at_base

# Announce
tellraw @a ["",{"selector":"@s","color":"green"},[{"text":" ","color":"green"}, {"translate":"mgs.joined_the_mission"}]]

