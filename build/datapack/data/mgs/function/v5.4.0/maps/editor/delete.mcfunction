
#> mgs:v5.4.0/maps/editor/delete
#
# @within	mgs:v5.4.0/dialog/close_then
#			string in mgs:v5.4.0/maps/editor/delete_confirm {idx:$(idx),mode:$(mode)}
#
# @args		mode (unknown)
#			idx (unknown)
#

$data remove storage mgs:maps $(mode)[$(idx)]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.map_deleted","fallback":"Map deleted.","color":"red"}]

$function mgs:v5.4.0/maps/editor/list/$(mode)

