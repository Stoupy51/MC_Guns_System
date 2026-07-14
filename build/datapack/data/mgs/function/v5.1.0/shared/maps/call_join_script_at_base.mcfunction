
#> mgs:v5.1.0/shared/maps/call_join_script_at_base
#
# @within	mgs:v5.1.0/zombies/join_game
#			mgs:v5.1.0/multiplayer/join_game
#			mgs:v5.1.0/missions/join_game
#

execute store result storage mgs:temp _base.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _base.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _base.z int 1 run scoreboard players get #gm_base_z mgs.data
data modify storage mgs:temp _base.fn set value "#mgs:maps/join_script"
function mgs:v5.1.0/shared/call_at_base with storage mgs:temp _base

