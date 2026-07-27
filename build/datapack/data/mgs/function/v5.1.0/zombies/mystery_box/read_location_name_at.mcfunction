
#> mgs:v5.1.0/zombies/mystery_box/read_location_name_at
#
# @within	mgs:v5.1.0/zombies/mystery_box/read_location_name with storage mgs:temp _mb_name_idx
#
# @args		idx (unknown)
#

$data modify storage mgs:zombies mystery_box.current_name set from storage mgs:zombies mystery_box.names[$(idx)]

