
#> mgs:v5.1.0/shared/maps/call_leave_script_at_base
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/stop [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/stop [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#

execute store result storage mgs:temp _base.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _base.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _base.z int 1 run scoreboard players get #gm_base_z mgs.data
data modify storage mgs:temp _base.fn set value "#mgs:maps/leave_script"
function mgs:v5.1.0/shared/call_at_base with storage mgs:temp _base

