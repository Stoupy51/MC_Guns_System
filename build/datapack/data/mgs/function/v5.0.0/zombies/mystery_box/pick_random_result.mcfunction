
#> mgs:v5.0.0/zombies/mystery_box/pick_random_result
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use
#			mgs:v5.0.0/zombies/mystery_box/reroll_owned
#

execute store result score #mb_pool_size mgs.data run data get storage mgs:zombies mystery_box_pool
execute if score #mb_pool_size mgs.data matches ..0 run return run function mgs:v5.0.0/zombies/mystery_box/deny_pool_empty
data modify storage bs:in random.weighted_choice.options set from storage mgs:zombies mystery_box_pool
data modify storage bs:in random.weighted_choice.weights set from storage mgs:zombies mystery_box_weights
function #bs.random:weighted_choice
data modify storage mgs:zombies mystery_box.result set from storage bs:out random.weighted_choice

