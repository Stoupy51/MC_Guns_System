
#> mgs:v5.0.0/zombies/mystery_box/pick_random_result
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use
#			mgs:v5.0.0/zombies/mystery_box/reroll_owned
#

execute store result score #mb_pool_size mgs.data run data get storage mgs:zombies mystery_box_pool
execute if score #mb_pool_size mgs.data matches ..0 run return run function mgs:v5.0.0/zombies/mystery_box/deny_pool_empty
execute store result score #mb_pick mgs.data run random value 0..1000000
scoreboard players operation #mb_pick mgs.data %= #mb_pool_size mgs.data
data modify storage mgs:temp _mb_pool_iter set from storage mgs:zombies mystery_box_pool
function mgs:v5.0.0/zombies/mystery_box/pick_item
data modify storage mgs:zombies mystery_box.result set from storage mgs:temp _mb_pool_iter[0]

