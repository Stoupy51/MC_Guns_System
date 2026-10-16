
#> mgs:v5.1.0/shared/summon_oob
#
# @within	mgs:v5.1.0/zombies/preload_complete {mode:"zombies"}
#			mgs:v5.1.0/missions/preload_complete {mode:"missions"}
#			mgs:v5.1.0/multiplayer/start {mode:"multiplayer"}
#
# @args		mode (string)
#

$function mgs:v5.1.0/shared/load_base_coordinates {mode:"$(mode)"}

$data modify storage mgs:temp _oob_iter set from storage mgs:$(mode) game.map.out_of_bounds
$data modify storage mgs:temp _oob_pos.mode set value "$(mode)"
execute if data storage mgs:temp _oob_iter[0] run function mgs:v5.1.0/shared/summon_oob_iter

