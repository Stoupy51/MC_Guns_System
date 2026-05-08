
#> mgs:v5.0.1/shared/maps/call_respawn_script_at_base
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.0.1/zombies/revive/do_round_respawn
#			mgs:v5.0.1/multiplayer/actual_respawn
#			mgs:v5.0.1/missions/actual_respawn
#

execute store result storage mgs:temp _base.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _base.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _base.z int 1 run scoreboard players get #gm_base_z mgs.data
data modify storage mgs:temp _base.fn set value "#mgs:maps/respawn_script"
function mgs:v5.0.1/shared/call_at_base with storage mgs:temp _base

