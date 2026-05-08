
#> mgs:v5.0.1/shared/maps/call_start_script_at_base
#
# @within	mgs:v5.0.1/zombies/end_prep
#			mgs:v5.0.1/multiplayer/end_prep
#			mgs:v5.0.1/missions/end_prep
#

execute store result storage mgs:temp _base.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _base.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _base.z int 1 run scoreboard players get #gm_base_z mgs.data
data modify storage mgs:temp _base.fn set value "#mgs:maps/start_script"
function mgs:v5.0.1/shared/call_at_base with storage mgs:temp _base

