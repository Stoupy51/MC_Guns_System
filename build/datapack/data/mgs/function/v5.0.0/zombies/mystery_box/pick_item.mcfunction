
#> mgs:v5.0.0/zombies/mystery_box/pick_item
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/pick_random_result
#			mgs:v5.0.0/zombies/mystery_box/pick_item
#

execute if score #mb_pick mgs.data matches 1.. run data remove storage mgs:temp _mb_pool_iter[0]
execute if score #mb_pick mgs.data matches 1.. run scoreboard players remove #mb_pick mgs.data 1
execute if score #mb_pick mgs.data matches 1.. run function mgs:v5.0.0/zombies/mystery_box/pick_item

