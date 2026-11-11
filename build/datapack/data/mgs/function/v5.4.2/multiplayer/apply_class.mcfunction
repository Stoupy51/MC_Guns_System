
#> mgs:v5.4.2/multiplayer/apply_class
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/start [ at @s ]
#			mgs:v5.4.2/multiplayer/prep_tick [ at @s ]
#			mgs:v5.4.2/multiplayer/join_game
#			mgs:v5.4.2/multiplayer/actual_respawn
#			mgs:v5.4.2/multiplayer/gamemodes/demo/start_round [ at @s ]
#			mgs:v5.4.2/multiplayer/gamemodes/snd/start_round [ at @s ]
#			mgs:v5.4.2/missions/preload_complete [ at @s ]
#			mgs:v5.4.2/missions/prep_tick [ at @s ]
#			mgs:v5.4.2/missions/join_game
#			mgs:v5.4.2/missions/actual_respawn
#			string in mgs:v5.4.2/multiplayer/set_class
#			mgs:v5.4.2/multiplayer/auto_apply_default
#			string in mgs:v5.4.2/multiplayer/custom/notify_selected
#

execute if score @s mgs.mp.class matches ..-1 run return run function mgs:v5.4.2/multiplayer/apply_custom_class

execute if score @s mgs.mp.class matches 1 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[0]
execute if score @s mgs.mp.class matches 2 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[1]
execute if score @s mgs.mp.class matches 3 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[2]
execute if score @s mgs.mp.class matches 4 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[3]
execute if score @s mgs.mp.class matches 5 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[4]
execute if score @s mgs.mp.class matches 6 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[5]
execute if score @s mgs.mp.class matches 7 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[6]
execute if score @s mgs.mp.class matches 8 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[7]
execute if score @s mgs.mp.class matches 9 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[8]
execute if score @s mgs.mp.class matches 10 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[9]

function mgs:v5.4.2/multiplayer/apply_class_dynamic

