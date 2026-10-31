
#> mgs:v5.3.0/zombies/mystery_box/build_pool
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/start
#

data modify storage mgs:zombies mystery_box_pool set value []
data modify storage mgs:zombies mystery_box_weights set value []
scoreboard players set #mb_ray_index mgs.data -1
data modify storage mgs:temp _mb_src set from storage mgs:config zombies.mystery_box_pool
execute if data storage mgs:zombies game.map.mystery_box_pool run data modify storage mgs:temp _mb_src set from storage mgs:zombies game.map.mystery_box_pool
function mgs:v5.3.0/zombies/mystery_box/build_pool_next

