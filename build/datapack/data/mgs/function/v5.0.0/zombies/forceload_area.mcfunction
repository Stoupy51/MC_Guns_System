
#> mgs:v5.0.0/zombies/forceload_area
#
# @within	mgs:v5.0.0/zombies/start
#

execute store result storage mgs:temp _fl.x1 int 1 run scoreboard players get #bound_x1 mgs.data
execute store result storage mgs:temp _fl.z1 int 1 run scoreboard players get #bound_z1 mgs.data
execute store result storage mgs:temp _fl.x2 int 1 run scoreboard players get #bound_x2 mgs.data
execute store result storage mgs:temp _fl.z2 int 1 run scoreboard players get #bound_z2 mgs.data
function mgs:v5.0.0/zombies/forceload_add with storage mgs:temp _fl

