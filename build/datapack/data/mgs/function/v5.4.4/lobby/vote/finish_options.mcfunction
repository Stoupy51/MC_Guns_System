
#> mgs:v5.4.4/lobby/vote/finish_options
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/multiplayer/open_vote {mode:"multiplayer"}
#			mgs:v5.4.4/lobby/multiplayer/map_round {mode:"multiplayer"}
#			mgs:v5.4.4/lobby/zombies/open_vote {mode:"zombies"}
#			mgs:v5.4.4/lobby/missions/open_vote {mode:"missions"}
#
# @args		mode (string)
#

$execute store result score #lv_slots mgs.data if data storage mgs:lobby $(mode).options[]
$execute if score #lv_slots mgs.data matches 2.. run data modify storage mgs:lobby $(mode).options append value {label:{translate:"mgs.random",fallback:"Random",color:"light_purple"},hover:{translate:"mgs.one_of_the_options_above_drawn_at_random",fallback:"One of the options above, drawn at random"},random:1b}
$execute store result score #lv_slots mgs.data if data storage mgs:lobby $(mode).options[]

