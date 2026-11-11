
#> mgs:v5.4.2/maps/editor/name/special_spawn_apply
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/name/special_spawn with storage mgs:temp _ed_name
#
# @args		group (unknown)
#			rounds (unknown)
#			entity (unknown)
#			arrival_flag (unknown)
#			power_flag (unknown)
#

$data modify entity @s data.name set value "Special Spawn $(group)$(rounds) $(entity)$(arrival_flag)$(power_flag)"
data modify entity @s CustomName set from entity @s data.name

