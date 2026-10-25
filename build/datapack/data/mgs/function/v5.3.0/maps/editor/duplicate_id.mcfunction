
#> mgs:v5.3.0/maps/editor/duplicate_id
#
# @within	mgs:v5.3.0/maps/editor/duplicate with storage mgs:temp _dup
#			mgs:v5.3.0/maps/editor/duplicate_id with storage mgs:temp _dup
#
# @args		id (unknown)
#			mode (unknown)
#

$data modify storage mgs:temp _dup.map.id set value "$(id)_copy"
data modify storage mgs:temp _dup.id set from storage mgs:temp _dup.map.id
$execute if data storage mgs:maps $(mode)[{id:"$(id)_copy"}] run function mgs:v5.3.0/maps/editor/duplicate_id with storage mgs:temp _dup

