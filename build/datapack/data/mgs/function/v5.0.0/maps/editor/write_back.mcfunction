
#> mgs:v5.0.0/maps/editor/write_back
#
# @executed	as @n[tag=mgs.new_element] & at @s
#
# @within	mgs:v5.0.0/maps/editor/do_save with storage mgs:temp map_edit
#
# @args		mode (unknown)
#			idx (unknown)
#

$data modify storage mgs:maps $(mode)[$(idx)] set from storage mgs:temp map_edit.map

