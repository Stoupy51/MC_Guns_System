
#> mgs:v5.4.1/multiplayer/reset_player
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/stop [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.4.1/stats/login
#

attribute @s minecraft:movement_speed base reset
attribute @s minecraft:jump_strength base reset
attribute @s minecraft:waypoint_receive_range base reset
effect clear @s darkness
effect clear @s blindness
effect clear @s night_vision
gamemode adventure @s[gamemode=spectator]

# The deciding kill's victim still shows its respawn countdown.
title @s clear

team leave @s
function mgs:v5.4.1/lobby/return
scoreboard players set @s mgs.mp.team 0
scoreboard players set @s mgs.mp.spectate_timer 0
scoreboard players set @s mgs.mp.in_game 0
tag @s remove mgs.give_class_menu
tag @s remove mgs.kc_viewer

