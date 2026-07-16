
#> mgs:v5.1.0/multiplayer/gamemodes/snd/start_round
#
# @executed	"","\ud83c\udfc6 ",{"translate":"mgs.score_limit"}],"tooltip":{"translate":"mgs.set_the_score_needed_to_win"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/score_limit"}},{"label":["","\u23f1 ",{"translate":"mgs.time_limit"}],"tooltip":{"translate":"mgs.set_the_match_time_limit"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/dialogs/multiplayer/setup/time_limit"}},{"label":["","\ud83d\uddfa ",{"translate":"mgs.select_map","color":"aqua"}],"tooltip":{"translate":"mgs.browse_and_select_a_map"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/map_select"}},{"label":["","\u25b6 ",{"translate":"mgs.start","color":"green"}],"tooltip":{"translate":"mgs.start_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/start"}},{"label":["","\u25a0 ",{"translate":"mgs.stop","color":"red"}],"tooltip":{"translate":"mgs.stop_the_match"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/stop"}},{"label":["","\u2694 ",{"translate":"mgs.classes","color":"aqua"}],"tooltip":{"translate":"mgs.select_your_class"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/select_class"}},{"label":["","+ ",{"translate":"mgs.join","color":"yellow"}],"tooltip":{"translate":"mgs.join_the_ongoing_game_as_a_late_joiner"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_game"}},{"label":{"translate":"mgs.red_team","color":"red"},"tooltip":{"translate":"mgs.join_red_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_red"}},{"label":{"translate":"mgs.blue_team","color":"blue"},"tooltip":{"translate":"mgs.join_blue_team"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/multiplayer/join_blue"}},{"label":{"translate":"mgs.auto_team","color":"yellow"},"tooltip":{"translate":"mgs.auto_balance_assign"},"action":{"type":"run_command","command":"/execute as @a[sort=random] run function mgs:v5.1.0/multiplayer/auto_assign_team"}},{"label":["","\ud83d\udc65 ",{"translate":"mgs.manage_players","color":"dark_aqua"}],"tooltip":{"translate":"mgs.assign_players_to_red_blue_teams"},"action":{"type":"run_command","command":"/function mgs:v5.1.0/players/list_multiplayer"}}
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/setup
#			mgs:v5.1.0/multiplayer/gamemodes/snd/next_round 60t [ scheduled ]
#

# Guard: only while the game is running (a scheduled call may fire after the game ended)
execute if data storage mgs:multiplayer game{state:"lobby"} run return fail
execute if data storage mgs:multiplayer game{state:"ended"} run return fail

# Announce round
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"────── ","color":"gold"}, {"translate":"mgs.round"}],{"score":{"name":"#snd_round","objective":"mgs.data"},"color":"yellow"},{"text":" ──────","color":"gold"}]

# Show which team attacks
execute if score #snd_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.attacks"}, " | "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.defends"}]]
execute if score #snd_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.attacks"}, " | "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.defends"}]]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Reset bomb state and channel progress
scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0
scoreboard players set #snd_plant_progress mgs.data 0
scoreboard players set #snd_defuse_progress mgs.data 0

# Reset round timer
scoreboard players set #snd_round_timer mgs.data 1800

# Restore players who died last round (S&D deaths skip the respawn countdown)
execute as @a[scores={mgs.mp.team=1..2},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={mgs.mp.team=1..2},gamemode=spectator]

# Tag alive players
tag @a[scores={mgs.mp.team=1..2},gamemode=!spectator] add mgs.snd_alive

# Teleport everyone to their team spawns and re-apply class loadouts
execute as @a[scores={mgs.mp.team=1}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"red"}
execute as @a[scores={mgs.mp.team=2}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"blue"}
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used
execute as @a[scores={mgs.mp.team=1..2}] at @s run function mgs:v5.1.0/multiplayer/apply_class

