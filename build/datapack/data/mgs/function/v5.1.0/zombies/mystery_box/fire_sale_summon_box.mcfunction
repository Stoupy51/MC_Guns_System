
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_summon_box
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/fire_sale_start [ as @e[tag=...] & at @s ]
#

data modify storage mgs:temp _mb_fs.yaw set value 0.0f
data modify storage mgs:temp _mb_fs.yaw set from entity @s Rotation[0]
function mgs:v5.1.0/zombies/mystery_box/summon_temp_box with storage mgs:temp _mb_fs

