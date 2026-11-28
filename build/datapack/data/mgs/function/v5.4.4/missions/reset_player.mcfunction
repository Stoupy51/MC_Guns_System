
#> mgs:v5.4.4/missions/reset_player
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.4.4/lobby/missions/leave
#

attribute @s minecraft:movement_speed base reset
attribute @s minecraft:jump_strength base reset
effect clear @s darkness
effect clear @s blindness
effect clear @s night_vision
gamemode adventure @s[gamemode=spectator]
clear @s compass[custom_data~{mgs:{compass:true}}]
function mgs:v5.4.4/shared/maps/call_script_at_base {mode:"missions",script:"leave"}
function mgs:v5.4.4/lobby/return
scoreboard players set @s mgs.mp.team 0
scoreboard players set @s mgs.mi.in_game 0

