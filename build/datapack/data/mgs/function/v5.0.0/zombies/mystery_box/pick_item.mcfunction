
#> mgs:v5.0.0/zombies/mystery_box/pick_item
#
# @executed	as @p[distance=..3,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use
#			mgs:v5.0.0/zombies/mystery_box/pick_item
#

execute if score #_mb_pick mgs.data matches 1.. run data remove storage mgs:temp _mb_pool_iter[0]
execute if score #_mb_pick mgs.data matches 1.. run scoreboard players remove #_mb_pick mgs.data 1
execute if score #_mb_pick mgs.data matches 1.. run function mgs:v5.0.0/zombies/mystery_box/pick_item

