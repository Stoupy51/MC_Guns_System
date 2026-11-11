
#> mgs:v5.4.2/zombies/mystery_box/build_pool
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/start
#

data modify storage mgs:zombies mystery_box_pool set value []
data modify storage mgs:zombies mystery_box_weights set value []
scoreboard players set #mb_ray_index mgs.data -1
data modify storage mgs:temp _mb_src set from storage mgs:config zombies.mystery_box_pool
execute if data storage mgs:zombies game.map.mystery_box_pool run data modify storage mgs:temp _mb_src set from storage mgs:zombies game.map.mystery_box_pool
function mgs:v5.4.2/zombies/mystery_box/build_pool_next

