
#> mgs:v5.3.0/zombies/mystery_box/build_pool_next
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/mystery_box/build_pool
#			mgs:v5.3.0/zombies/mystery_box/build_pool_next
#

execute unless data storage mgs:temp _mb_src[0] run return 0

execute store result score #mb_w mgs.data run data get storage mgs:temp _mb_src[0].weight
execute if score #mb_w mgs.data matches 1.. run function mgs:v5.3.0/zombies/mystery_box/build_pool_add with storage mgs:temp _mb_src[0]

data remove storage mgs:temp _mb_src[0]
function mgs:v5.3.0/zombies/mystery_box/build_pool_next

