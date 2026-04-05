
#> mgs:v5.0.0/shared/summon_oob
#
# @within	mgs:v5.0.0/zombies/preload_complete {mode:"zombies"}
#			mgs:v5.0.0/multiplayer/start {mode:"multiplayer"}
#			mgs:v5.0.0/missions/preload_complete {mode:"missions"}
#
# @args		mode (string)
#

$function mgs:v5.0.0/shared/load_base_coordinates {mode:"$(mode)"}

$data modify storage mgs:temp _oob_iter set from storage mgs:$(mode) game.map.out_of_bounds
execute if data storage mgs:temp _oob_iter[0] run function mgs:v5.0.0/shared/summon_oob_iter

