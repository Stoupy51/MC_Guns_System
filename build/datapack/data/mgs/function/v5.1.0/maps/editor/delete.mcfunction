
#> mgs:v5.1.0/maps/editor/delete
#
# @within	string in mgs:v5.1.0/maps/editor/menu_entry_display
#
# @args		mode (unknown)
#			idx (unknown)
#

$data remove storage mgs:maps $(mode)[$(idx)]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_deleted","color":"red"}]

# Refresh menu for the same mode
$function mgs:v5.1.0/maps/editor/list/$(mode)

