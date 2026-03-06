
#> mgs:v5.0.0/maps/editor/delete
#
# @within	???
#
# @args		mode (unknown)
#			idx (unknown)
#

$data remove storage mgs:maps $(mode)[$(idx)]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.map_deleted","color":"red"}]

# Refresh menu for the same mode
$function mgs:v5.0.0/maps/editor/list/$(mode)

