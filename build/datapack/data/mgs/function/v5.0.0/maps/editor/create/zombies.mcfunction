
#> mgs:v5.0.0/maps/editor/create/zombies
#
# @within	???
#

tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s [{"text":"","color":"gold","bold":true},"  📝 ",{"translate":"mgs.create_new_zombies_map"}]
tellraw @s {"text":"============================================","color":"dark_gray"}
tellraw @s {"translate":"mgs.run_this_command_to_create_a_new_map","color":"yellow"}
tellraw @s [{"text":"","color":"aqua","click_event":{"action":"suggest_command","command":"/data modify storage mgs:maps zombies append value {id:'my_map',name:'My Map',description:'A new map',base_coordinates:[0,64,0],start_commands:[],respawn_commands:[]}"}},"/data modify storage mgs:maps zombies append value {...}"]
tellraw @s ["  ",{"translate":"mgs.click_to_paste_the_command_then_edit_the_id_name_description","color":"gray","italic":true}]
tellraw @s ""
tellraw @s ["  ",[{"text": "[", "color": "yellow", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.0.0/maps/editor/list/zombies"}, "hover_event": {"action": "show_text", "value": "Back to map list"}}, "\u25c0 Back", "]"]]
tellraw @s {"text":"============================================","color":"dark_gray"}

