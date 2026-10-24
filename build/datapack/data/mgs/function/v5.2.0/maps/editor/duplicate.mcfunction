
#> mgs:v5.2.0/maps/editor/duplicate
#
# @within	string in mgs:v5.2.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}
#
# @args		mode (unknown)
#			idx (unknown)
#

$data modify storage mgs:temp _dup.map set from storage mgs:maps $(mode)[$(idx)]
$data modify storage mgs:temp _dup.mode set value "$(mode)"
data modify storage mgs:temp _dup.id set from storage mgs:temp _dup.map.id
function mgs:v5.2.0/maps/editor/duplicate_id with storage mgs:temp _dup
$data modify storage mgs:maps $(mode) append from storage mgs:temp _dup.map
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.map_duplicated_as","fallback":"Map duplicated as ","color":"green"},{"storage":"mgs:temp","nbt":"_dup.map.id","color":"white"}]
$function mgs:v5.2.0/maps/editor/list/$(mode)

