
#> mgs:v5.2.0/shared/maps/call_script_at_base
#
# @within	mgs:v5.2.0/zombies/end_prep {mode:"zombies",script:"start"}
#			mgs:v5.2.0/zombies/game_tick {mode:"zombies",script:"tick"}
#			mgs:v5.2.0/zombies/join_game {mode:"zombies",script:"join"}
#			mgs:v5.2.0/multiplayer/end_prep {mode:"multiplayer",script:"start"}
#			mgs:v5.2.0/multiplayer/game_tick {mode:"multiplayer",script:"tick"}
#			mgs:v5.2.0/multiplayer/join_game {mode:"multiplayer",script:"join"}
#			mgs:v5.2.0/multiplayer/actual_respawn {mode:"multiplayer",script:"respawn"}
#			mgs:v5.2.0/multiplayer/stop {mode:"multiplayer",script:"leave"} [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.2.0/missions/end_prep {mode:"missions",script:"start"}
#			mgs:v5.2.0/missions/game_tick {mode:"missions",script:"tick"}
#			mgs:v5.2.0/missions/join_game {mode:"missions",script:"join"}
#			mgs:v5.2.0/missions/actual_respawn {mode:"missions",script:"respawn"}
#			mgs:v5.2.0/missions/stop {mode:"missions",script:"leave"} [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.2.0/zombies/reset_player {mode:"zombies",script:"leave"}
#			mgs:v5.2.0/zombies/power/on_activate {mode:"zombies",script:"power"}
#			mgs:v5.2.0/zombies/revive/do_round_respawn {mode:"zombies",script:"respawn"}
#
# @args		mode (string)
#			script (string)
#

$execute store result storage mgs:temp _base.x int 1 run scoreboard players get #$(mode)_base_x mgs.data
$execute store result storage mgs:temp _base.y int 1 run scoreboard players get #$(mode)_base_y mgs.data
$execute store result storage mgs:temp _base.z int 1 run scoreboard players get #$(mode)_base_z mgs.data
$data modify storage mgs:temp _base.mode set value "$(mode)"
$data modify storage mgs:temp _base.fn set value "#mgs:maps/$(script)_script"
function mgs:v5.2.0/shared/call_at_base with storage mgs:temp _base

$execute unless data storage mgs:$(mode) game.map.$(script)_command run return 0
$data modify storage mgs:temp _base.command set from storage mgs:$(mode) game.map.$(script)_command
function mgs:v5.2.0/shared/run_start_command with storage mgs:temp _base

