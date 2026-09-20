
#> mgs:v5.1.0/shared/maps/call_script_at_base
#
# @within	mgs:v5.1.0/zombies/end_prep {script:"start"}
#			mgs:v5.1.0/zombies/game_tick {script:"tick"}
#			mgs:v5.1.0/zombies/stop {script:"leave"} [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.1.0/zombies/join_game {script:"join"}
#			mgs:v5.1.0/zombies/power/on_activate {script:"power"}
#			mgs:v5.1.0/zombies/revive/do_round_respawn {script:"respawn"}
#			mgs:v5.1.0/multiplayer/stop {script:"leave"} [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/join_game {script:"join"}
#			mgs:v5.1.0/multiplayer/game_tick {script:"tick"}
#			mgs:v5.1.0/multiplayer/end_prep {script:"start"}
#			mgs:v5.1.0/multiplayer/actual_respawn {script:"respawn"}
#			mgs:v5.1.0/missions/end_prep {script:"start"}
#			mgs:v5.1.0/missions/actual_respawn {script:"respawn"}
#			mgs:v5.1.0/missions/game_tick {script:"tick"}
#			mgs:v5.1.0/missions/stop {script:"leave"} [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.1.0/missions/join_game {script:"join"}
#
# @args		script (string)
#

execute store result storage mgs:temp _base.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _base.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _base.z int 1 run scoreboard players get #gm_base_z mgs.data
$data modify storage mgs:temp _base.fn set value "#mgs:maps/$(script)_script"
function mgs:v5.1.0/shared/call_at_base with storage mgs:temp _base

