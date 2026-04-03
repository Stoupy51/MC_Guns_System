
#> mgs:v5.0.0/missions/stop
#
# @within	mgs:v5.0.0/missions/victory
#			mgs:v5.0.0/missions/setup "hover_event": {"action": "show_text", "value": "Start the mission"}}, "\u25b6 START", "]"]," ",[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/missions/stop"}, "hover_event": {"action": "show_text", "value": "Stop the mission"}}, "\u25a0 STOP", "]"]," ",[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/multiplayer/select_class"}, "hover_event": {"action": "show_text", "value": "Select your class"}}, "\u2694 Classes", "]"]]
#

# Set state to lobby
data modify storage mgs:missions game.state set value "lobby"

# Cancel scheduled functions
schedule clear mgs:v5.0.0/missions/end_prep

# Restore movement
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:movement_speed base set 0.1
execute as @a[scores={mgs.mi.in_game=1}] run attribute @s minecraft:jump_strength base set 0.42

# Clear effects
effect clear @a[scores={mgs.mi.in_game=1}] darkness
effect clear @a[scores={mgs.mi.in_game=1}] blindness
effect clear @a[scores={mgs.mi.in_game=1}] night_vision

# Remove compass from all players
clear @a[scores={mgs.mi.in_game=1}] compass[custom_data~{mgs:{compass:true}}]

# Kill all mission entities (enemies + markers)
kill @e[tag=mgs.mission_enemy]
kill @e[tag=mgs.gm_entity]

# Remove forceload
execute if score #mi_has_boundary mgs.data matches 1 run function mgs:v5.0.0/shared/remove_forceload

# Signal mission end
function #mgs:missions/on_mission_end

# Announce
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mission_ended","color":"red"}]

# Reset in-game state
scoreboard players set @a[scores={mgs.mi.in_game=1}] mgs.mp.team 0
scoreboard players set @a mgs.mi.in_game 0
scoreboard players set #mi_timer mgs.data 0
scoreboard players set #mi_total_enemies mgs.data 0
scoreboard players set #mi_has_boundary mgs.data 0
scoreboard players set @a mgs.mi.kills 0
scoreboard players set @a mgs.mi.deaths 0
tag @a[tag=mgs.give_class_menu] remove mgs.give_class_menu

