
#> mgs:v5.0.0/zombies/powerups/activate/free_pap
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/dispatch_activate
#

execute as @p[tag=mgs.pu_collecting] run function mgs:v5.0.0/zombies/pap/on_free_pap

