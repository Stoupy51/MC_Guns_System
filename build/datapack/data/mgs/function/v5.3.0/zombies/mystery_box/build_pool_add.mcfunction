
#> mgs:v5.3.0/zombies/mystery_box/build_pool_add
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/mystery_box/build_pool_next with storage mgs:temp _mb_src[0]
#
# @args		weapon_id (unknown)
#

$execute unless data storage mgs:zombies mystery_box_catalog.$(weapon_id) run return fail

$data modify storage mgs:temp _mb_id set value "$(weapon_id)"
execute if data storage mgs:temp {_mb_id:"ray_gun"} store result score #mb_ray_index mgs.data run data get storage mgs:zombies mystery_box_pool
execute if data storage mgs:temp {_mb_id:"ray_gun"} run scoreboard players operation #mb_ray_weight mgs.data = #mb_w mgs.data
$data modify storage mgs:zombies mystery_box_pool append from storage mgs:zombies mystery_box_catalog.$(weapon_id)
data modify storage mgs:zombies mystery_box_weights append value 0
execute store result storage mgs:zombies mystery_box_weights[-1] int 1 run scoreboard players get #mb_w mgs.data

