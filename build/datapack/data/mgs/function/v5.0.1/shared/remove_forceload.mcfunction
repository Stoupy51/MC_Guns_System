
#> mgs:v5.0.1/shared/remove_forceload
#
# @within	mgs:v5.0.1/zombies/stop
#			mgs:v5.0.1/missions/stop
#

execute store result storage mgs:temp _fl.x1 int 1 run scoreboard players get #bound_x1 mgs.data
execute store result storage mgs:temp _fl.z1 int 1 run scoreboard players get #bound_z1 mgs.data
execute store result storage mgs:temp _fl.x2 int 1 run scoreboard players get #bound_x2 mgs.data
execute store result storage mgs:temp _fl.z2 int 1 run scoreboard players get #bound_z2 mgs.data
function mgs:v5.0.1/shared/forceload_remove with storage mgs:temp _fl

