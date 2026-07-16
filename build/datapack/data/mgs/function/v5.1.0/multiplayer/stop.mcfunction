
#> mgs:v5.1.0/multiplayer/stop
#
# @within	mgs:v5.1.0/multiplayer/team_wins
#			mgs:v5.1.0/multiplayer/game_draw
#			mgs:v5.1.0/multiplayer/gamemodes/ffa/player_wins
#			mgs:v5.1.0/dialogs/multiplayer/setup {"label": ["", "\ud83c\udfc6 ", {"translate": "mgs.score_limit"}], "tooltip": {"translate": "mgs.set_the_score_needed_to_win"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}}, {"label": ["", "\u23f1 ", {"translate": "mgs.time_limit"}], "tooltip": {"translate": "mgs.set_the_match_time_limit"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}}, {"label": ["", "\ud83d\uddfa ", {"translate": "mgs.select_map", "color": "aqua"}], "tooltip": {"translate": "mgs.browse_and_select_a_map"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/map_select"}}, {"label": ["", "\u25b6 ", {"translate": "mgs.start", "color": "green"}], "tooltip": {"translate": "mgs.start_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/start"}}, {"label": ["", "\u25a0 ", {"translate": "mgs.stop", "color": "red"}], "tooltip": {"translate": "mgs.stop_the_match"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/stop"}}, {"label": ["", "\u2694 ", {"translate": "mgs.classes", "color": "aqua"}], "tooltip": {"translate": "mgs.select_your_class"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/select_class"}}, {"label": ["", "+ ", {"translate": "mgs.join", "color": "yellow"}], "tooltip": {"translate": "mgs.join_the_ongoing_game_as_a_late_joiner"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_game"}}, {"label": {"translate": "mgs.red_team", "color": "red"}, "tooltip": {"translate": "mgs.join_red_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_red"}}, {"label": {"translate": "mgs.blue_team", "color": "blue"}, "tooltip": {"translate": "mgs.join_blue_team"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/multiplayer/join_blue"}}, {"label": {"translate": "mgs.auto_team", "color": "yellow"}, "tooltip": {"translate": "mgs.auto_balance_assign"}, "action": {"type": "run_command", "command": "/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}}, {"label": ["", "\ud83d\udc65 ", {"translate": "mgs.manage_players", "color": "dark_aqua"}], "tooltip": {"translate": "mgs.assign_players_to_red_blue_teams"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/players/list_multiplayer"}}], "columns": 2, "exit_action": {"label": {"text": "\u25c0 Back", "color": "gray"}, "tooltip": {"translate": "mgs.return_to_the_game_modes_menu"}, "action": {"type": "run_command", "command": "/function mgs:v5.1.0/dialogs/config/modes"}}}
#

# Various cleanup to go back to lobby
data modify storage mgs:multiplayer game.state set value "lobby"
schedule clear mgs:v5.1.0/multiplayer/end_prep
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base reset
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:waypoint_receive_range base reset
effect clear @a[scores={mgs.mp.in_game=1}] darkness
effect clear @a[scores={mgs.mp.in_game=1}] blindness
effect clear @a[scores={mgs.mp.in_game=1}] night_vision
gamemode adventure @a[scores={mgs.mp.in_game=1},gamemode=spectator]
kill @e[tag=mgs.gm_entity]
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.1.0/multiplayer/gamemodes/ffa/cleanup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.1.0/multiplayer/gamemodes/tdm/cleanup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.1.0/multiplayer/gamemodes/dom/cleanup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.1.0/multiplayer/gamemodes/hp/cleanup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.1.0/multiplayer/gamemodes/snd/cleanup
function #mgs:multiplayer/on_game_end

# Re-enable natural regeneration, disable custom regen system
gamerule natural_health_regeneration true
scoreboard players set #any_game_active mgs.data 0

# Tear down stamina state: stop any hunger drain and refill the bar so nobody is left winded
effect clear @a minecraft:hunger
effect give @a minecraft:saturation 5 20 true
scoreboard players set @a mgs.stam_out 0
scoreboard players set @a mgs.stam_seen 0

# Announce scores (team scores are meaningless in FFA — the winner is announced by player_wins)
tellraw @a ["","⚔ ",[{"text":"","color":"gold","bold":true},{"translate":"mgs.game_over"},"! "]]
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run tellraw @a ["",{"translate":"mgs.red","color":"red"},{"text":": "},{"score":{"name":"#red","objective":"mgs.mp.team"}}," | ",{"translate":"mgs.blue","color":"blue"},{"text":": "},{"score":{"name":"#blue","objective":"mgs.mp.team"}}]

# Remove sidebar and list displays and leave teams
scoreboard objectives setdisplay sidebar
scoreboard objectives remove mgs.sidebar
scoreboard objectives setdisplay list
team leave @a[team=mgs.red]
team leave @a[team=mgs.blue]

# Call map leave script for each in-game player (state is still active/preparing here)
execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.1.0/shared/maps/call_leave_script_at_base

scoreboard players set @a mgs.mp.in_game 0
scoreboard players set @a mgs.mp.team 0
scoreboard players set @a mgs.mp.spectate_timer 0
scoreboard players set #mp_has_boundary mgs.data 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

