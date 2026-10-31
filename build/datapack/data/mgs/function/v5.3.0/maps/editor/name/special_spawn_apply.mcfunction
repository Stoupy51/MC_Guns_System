
#> mgs:v5.3.0/maps/editor/name/special_spawn_apply
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/name/special_spawn with storage mgs:temp _ed_name
#
# @args		group (unknown)
#			rounds (unknown)
#			entity (unknown)
#			arrival_flag (unknown)
#			power_flag (unknown)
#

$data modify entity @s CustomName set value "Special Spawn $(group)$(rounds) $(entity)$(arrival_flag)$(power_flag)"

