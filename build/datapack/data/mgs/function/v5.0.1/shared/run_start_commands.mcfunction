
#> mgs:v5.0.1/shared/run_start_commands
#
# @within	mgs:v5.0.1/zombies/preload_complete {mode:"zombies"}
#			mgs:v5.0.1/multiplayer/start {mode:"multiplayer"}
#			mgs:v5.0.1/missions/end_prep {mode:"missions"}
#
# @args		mode (string)
#

$data modify storage mgs:temp _start_cmd_iter set from storage mgs:$(mode) game.map.start_commands
execute if data storage mgs:temp _start_cmd_iter[0] run function mgs:v5.0.1/shared/run_start_commands_iter

