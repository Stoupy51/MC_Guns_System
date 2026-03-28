
#> mgs:v5.0.0/maps/editor/handle_respawn_command
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/process_element
#

# Get position for permanent marker
execute store result storage mgs:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function mgs:v5.0.0/maps/editor/summon_respawn_command_marker with storage mgs:temp _pos

# Set default command on marker
execute as @n[tag=mgs.new_respawn_cmd_marker] run data modify entity @s data.command set value "effect give @s minecraft:speed 5 0 true"
tag @e[tag=mgs.new_respawn_cmd_marker] remove mgs.new_respawn_cmd_marker

# Announce + quick edit helper
tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.respawn_command_placed","color":"dark_aqua"}]
tellraw @a[tag=mgs.map_editor] ["  ",[{"text": "[", "color": "dark_aqua", "click_event": {"action": "suggest_command", "command": "/data modify entity @n[tag=mgs.element.respawn_command,distance=..10] data.command set value \"effect give @s minecraft:speed 5 0 true\""}, "hover_event": {"action": "show_text", "value": "Click to edit the command to run when players respawn"}}, "Edit Command", "]"]]

