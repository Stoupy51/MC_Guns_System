
#> mgs:v5.3.0/shared/enter_map
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/start {mode:"zombies",fn:"mgs:v5.3.0/zombies/start"}
#			mgs:v5.3.0/zombies/preload_complete {mode:"zombies",fn:"mgs:v5.3.0/zombies/preload_complete"}
#			mgs:v5.3.0/zombies/end_prep {mode:"zombies",fn:"mgs:v5.3.0/zombies/end_prep"}
#			mgs:v5.3.0/zombies/game_tick {mode:"zombies",fn:"mgs:v5.3.0/zombies/game_tick"}
#			mgs:v5.3.0/zombies/freeze_tick {mode:"zombies",fn:"mgs:v5.3.0/zombies/freeze_tick"}
#			mgs:v5.3.0/zombies/join_game {mode:"zombies",fn:"mgs:v5.3.0/zombies/join_game"}
#			mgs:v5.3.0/zombies/respawn_tp {mode:"zombies",fn:"mgs:v5.3.0/zombies/respawn_tp"}
#			mgs:v5.3.0/zombies/stop {mode:"zombies",fn:"mgs:v5.3.0/zombies/stop"}
#			mgs:v5.3.0/multiplayer/start {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/start"}
#			mgs:v5.3.0/multiplayer/end_prep {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/end_prep"}
#			mgs:v5.3.0/multiplayer/prep_tick {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/prep_tick"}
#			mgs:v5.3.0/multiplayer/game_tick {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/game_tick"}
#			mgs:v5.3.0/multiplayer/join_game {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/join_game"}
#			mgs:v5.3.0/multiplayer/respawn_tp {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/respawn_tp"}
#			mgs:v5.3.0/multiplayer/actual_respawn {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/actual_respawn"}
#			mgs:v5.3.0/multiplayer/gamemodes/demo/start_round {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/gamemodes/demo/start_round"}
#			mgs:v5.3.0/multiplayer/gamemodes/snd/start_round {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/gamemodes/snd/start_round"}
#			mgs:v5.3.0/multiplayer/stop {mode:"multiplayer",fn:"mgs:v5.3.0/multiplayer/stop"}
#			mgs:v5.3.0/missions/start {mode:"missions",fn:"mgs:v5.3.0/missions/start"}
#			mgs:v5.3.0/missions/preload_complete {mode:"missions",fn:"mgs:v5.3.0/missions/preload_complete"}
#			mgs:v5.3.0/missions/end_prep {mode:"missions",fn:"mgs:v5.3.0/missions/end_prep"}
#			mgs:v5.3.0/missions/prep_tick {mode:"missions",fn:"mgs:v5.3.0/missions/prep_tick"}
#			mgs:v5.3.0/missions/game_tick {mode:"missions",fn:"mgs:v5.3.0/missions/game_tick"}
#			mgs:v5.3.0/missions/join_game {mode:"missions",fn:"mgs:v5.3.0/missions/join_game"}
#			mgs:v5.3.0/missions/respawn_tp {mode:"missions",fn:"mgs:v5.3.0/missions/respawn_tp"}
#			mgs:v5.3.0/missions/actual_respawn {mode:"missions",fn:"mgs:v5.3.0/missions/actual_respawn"}
#			mgs:v5.3.0/missions/stop {mode:"missions",fn:"mgs:v5.3.0/missions/stop"}
#
# @args		mode (string)
#			fn (string)
#

$scoreboard players set #in_$(mode)_map mgs.data 1
$function mgs:v5.3.0/shared/use_map_frame {mode:"$(mode)"}
$data modify storage mgs:temp _enter set value {mode:"$(mode)",fn:"$(fn)",dimension:"minecraft:overworld"}
$data modify storage mgs:temp _enter.map_id set from storage mgs:$(mode) game.map_id
function mgs:v5.3.0/shared/enter_map_dimension with storage mgs:temp _enter
function mgs:v5.3.0/shared/enter_map_run with storage mgs:temp _enter
$scoreboard players set #in_$(mode)_map mgs.data 0

