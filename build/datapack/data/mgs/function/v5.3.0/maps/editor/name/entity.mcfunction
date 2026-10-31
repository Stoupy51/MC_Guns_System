
#> mgs:v5.3.0/maps/editor/name/entity
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/refresh_marker
#

data modify storage mgs:temp _ed_name.entity set from entity @s data.mob.entity
data modify storage mgs:temp _ed_name.prefix set value ""
data modify storage mgs:temp _ed_name.prefix set string storage mgs:temp _ed_name.entity 0 10
execute if data storage mgs:temp _ed_name{prefix:"minecraft:"} run data modify storage mgs:temp _ed_name.entity set string storage mgs:temp _ed_name.entity 10

