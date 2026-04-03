
#> mgs:v5.0.0/multiplayer/stop
#
# @within	mgs:v5.0.0/multiplayer/team_wins
#			mgs:v5.0.0/multiplayer/game_draw
#			mgs:v5.0.0/multiplayer/gamemodes/ffa/player_wins
#			mgs:v5.0.0/multiplayer/setup "hover_event": {"action": "show_text", "value": "Start the match"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/stop"}, "hover_event": {"action": "show_text", "value": "Stop the match"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/select_class"}, "hover_event": {"action": "show_text", "value": "Select your class"}}, "\u2694 Classes", "]"]]
#

# End game
data modify storage mgs:multiplayer game.state set value "lobby"

# Cancel scheduled prep end (in case game stopped during prep)
schedule clear mgs:v5.0.0/multiplayer/end_prep

# Restore movement (in case stopped during prep)
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.mp.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear prep effects (in case stopped during prep)
effect clear @a[scores={mgs.mp.in_game=1}] darkness
effect clear @a[scores={mgs.mp.in_game=1}] blindness
effect clear @a[scores={mgs.mp.in_game=1}] night_vision

# Gamemode cleanup
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.0.0/multiplayer/gamemodes/ffa/cleanup
execute if data storage mgs:multiplayer game{gamemode:"tdm"} run function mgs:v5.0.0/multiplayer/gamemodes/tdm/cleanup
execute if data storage mgs:multiplayer game{gamemode:"dom"} run function mgs:v5.0.0/multiplayer/gamemodes/dom/cleanup
execute if data storage mgs:multiplayer game{gamemode:"hp"} run function mgs:v5.0.0/multiplayer/gamemodes/hp/cleanup
execute if data storage mgs:multiplayer game{gamemode:"snd"} run function mgs:v5.0.0/multiplayer/gamemodes/snd/cleanup

# Restore all spectating players to adventure mode
gamemode adventure @a[scores={mgs.mp.in_game=1},gamemode=spectator]

# Kill gamemode entities
kill @e[tag=mgs.gm_entity]

# Signal game end
function #mgs:multiplayer/on_game_end

# Announce scores
tellraw @a ["",[{"text":"","color":"gold","bold":true},"⚔ ",{"translate":"mgs.game_over"},"! "]]
tellraw @a ["",{"translate":"mgs.red","color":"red"},{"text":": "},{"score":{"name":"#red","objective":"mgs.mp.team"}}," | ",{"translate":"mgs.blue","color":"blue"},{"text":": "},{"score":{"name":"#blue","objective":"mgs.mp.team"}}]

# Remove sidebar and list displays
scoreboard objectives setdisplay sidebar
scoreboard objectives remove mgs.sidebar
scoreboard objectives setdisplay list

# Clear in-game state
scoreboard players set @a mgs.mp.in_game 0
scoreboard players set @a mgs.mp.team 0
scoreboard players set @a mgs.mp.spectate_timer 0
scoreboard players set #mp_has_boundary mgs.data 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

