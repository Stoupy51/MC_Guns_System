
#> mgs:v5.1.0/shared/maps/call_power_script_at_base
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.1.0/zombies/power/on_activate
#

execute store result storage mgs:temp _base.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _base.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _base.z int 1 run scoreboard players get #gm_base_z mgs.data
data modify storage mgs:temp _base.fn set value "#mgs:maps/power_script"
function mgs:v5.1.0/shared/call_at_base with storage mgs:temp _base

