
#> mgs:v5.4.1/shared/enter_map
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/start {mode:"zombies",fn:"mgs:v5.4.1/zombies/start"}
#			mgs:v5.4.1/zombies/preload_complete {mode:"zombies",fn:"mgs:v5.4.1/zombies/preload_complete"}
#			mgs:v5.4.1/zombies/end_prep {mode:"zombies",fn:"mgs:v5.4.1/zombies/end_prep"}
#			mgs:v5.4.1/zombies/game_tick {mode:"zombies",fn:"mgs:v5.4.1/zombies/game_tick"}
#			mgs:v5.4.1/zombies/freeze_tick {mode:"zombies",fn:"mgs:v5.4.1/zombies/freeze_tick"}
#			mgs:v5.4.1/zombies/join_game {mode:"zombies",fn:"mgs:v5.4.1/zombies/join_game"}
#			mgs:v5.4.1/zombies/respawn_tp {mode:"zombies",fn:"mgs:v5.4.1/zombies/respawn_tp"}
#			mgs:v5.4.1/zombies/stop {mode:"zombies",fn:"mgs:v5.4.1/zombies/stop"}
#			mgs:v5.4.1/multiplayer/start {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/start"}
#			mgs:v5.4.1/multiplayer/end_prep {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/end_prep"}
#			mgs:v5.4.1/multiplayer/prep_tick {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/prep_tick"}
#			mgs:v5.4.1/multiplayer/game_tick {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/game_tick"}
#			mgs:v5.4.1/multiplayer/join_game {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/join_game"}
#			mgs:v5.4.1/multiplayer/respawn_tp {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/respawn_tp"}
#			mgs:v5.4.1/multiplayer/actual_respawn {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/actual_respawn"}
#			mgs:v5.4.1/multiplayer/gamemodes/demo/start_round {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/gamemodes/demo/start_round"}
#			mgs:v5.4.1/multiplayer/gamemodes/snd/start_round {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/gamemodes/snd/start_round"}
#			mgs:v5.4.1/multiplayer/kill_cam/tick {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/kill_cam/tick"}
#			mgs:v5.4.1/multiplayer/stop {mode:"multiplayer",fn:"mgs:v5.4.1/multiplayer/stop"}
#			mgs:v5.4.1/missions/start {mode:"missions",fn:"mgs:v5.4.1/missions/start"}
#			mgs:v5.4.1/missions/preload_complete {mode:"missions",fn:"mgs:v5.4.1/missions/preload_complete"}
#			mgs:v5.4.1/missions/end_prep {mode:"missions",fn:"mgs:v5.4.1/missions/end_prep"}
#			mgs:v5.4.1/missions/prep_tick {mode:"missions",fn:"mgs:v5.4.1/missions/prep_tick"}
#			mgs:v5.4.1/missions/game_tick {mode:"missions",fn:"mgs:v5.4.1/missions/game_tick"}
#			mgs:v5.4.1/missions/join_game {mode:"missions",fn:"mgs:v5.4.1/missions/join_game"}
#			mgs:v5.4.1/missions/respawn_tp {mode:"missions",fn:"mgs:v5.4.1/missions/respawn_tp"}
#			mgs:v5.4.1/missions/actual_respawn {mode:"missions",fn:"mgs:v5.4.1/missions/actual_respawn"}
#			mgs:v5.4.1/missions/stop {mode:"missions",fn:"mgs:v5.4.1/missions/stop"}
#
# @args		mode (string)
#			fn (string)
#

$scoreboard players set #in_$(mode)_map mgs.data 1
$function mgs:v5.4.1/shared/use_map_frame {mode:"$(mode)"}
$data modify storage mgs:temp _enter set value {mode:"$(mode)",fn:"$(fn)",dimension:"minecraft:overworld"}
$data modify storage mgs:temp _enter.map_id set from storage mgs:$(mode) game.map_id
function mgs:v5.4.1/shared/enter_map_dimension with storage mgs:temp _enter
function mgs:v5.4.1/shared/enter_map_run with storage mgs:temp _enter
$scoreboard players set #in_$(mode)_map mgs.data 0

