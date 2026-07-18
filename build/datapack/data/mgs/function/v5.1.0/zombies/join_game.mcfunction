
#> mgs:v5.1.0/zombies/join_game
#
# @within	mgs:v5.1.0/players/zb_join
#			mgs:v5.1.0/dialogs/zombies/setup {"label": ["", "\ud83e\uddec ", {"translate": "mgs.variant"}], "tooltip": {"translate": "mgs.choose_the_zombies_experience"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/zombies/setup/variant"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/stop"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.add_or_remove_players_from_the_zombies_game"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_zombies"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.all_players_join", "color": "green"}], "tooltip": {"translate": "mgs.add_every_online_player_to_the_zombies_game"}, "action": {"type": "run_command", "command": "/execute as @a run function mgs:v5.1.0/players/zb_join"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_zombies_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/zombies/join_game"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_configuration_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config"}}}
#

# Require an active game
execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_active_zombies_game_to_join","color":"red"}]

# Prevent double-joining
execute if score @s mgs.zb.in_game matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_are_already_in_the_zombies_game","color":"red"}]

# Tag as in-game and reset stats
scoreboard players set @s mgs.zb.in_game 1
team join mgs.zombies @s
scoreboard players set @s mgs.zb.points 500
scoreboard players set @s mgs.zb.kills 0
scoreboard players set @s mgs.zb.downs 0
scoreboard players set @s mgs.zb.passive 0
scoreboard players set @s mgs.zb.ability 0
scoreboard players set @s mgs.zb.ability_cd 0
scoreboard players set @s mgs.mp.spectate_timer 0
scoreboard players set @s mgs.mp.death_count 0
attribute @s minecraft:max_health base reset
attribute @s minecraft:entity_interaction_range base set 5

# Setup player
gamemode adventure @s

# Reset stamina so the stamina system re-inits this player at full (it owns the hunger bar)
scoreboard players set @s mgs.stam_seen 0

# Zombies has no class selection: give the fixed starting loadout (knife + pistol), matching the start function
function mgs:v5.1.0/zombies/inventory/give_starting_loadout

scoreboard players operation @s mgs.zb.prev_kills = @s mgs.total_kills

# Teleport to spawn
function mgs:v5.1.0/zombies/respawn_tp

# Call map join script (executed as the joining player)
function mgs:v5.1.0/shared/maps/call_join_script_at_base

# Announce
tellraw @a ["",{"selector":"@s","color":"dark_green"},[{"text":" ","color":"dark_green"}, {"translate":"mgs.joined_the_zombies_game"}]]

