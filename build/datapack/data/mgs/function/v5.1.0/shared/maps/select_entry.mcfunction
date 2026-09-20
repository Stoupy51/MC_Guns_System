
#> mgs:v5.1.0/shared/maps/select_entry
#
# @within	mgs:v5.1.0/shared/maps/select_iter with storage mgs:temp _map_entry
#
# @args		name (unknown)
#			description (unknown)
#			mode (unknown)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"green"},tooltip:{text:"$(description)"},action:{type:"run_command",command:"/data modify storage mgs:$(mode) game.map_id set value \"$(id)\""}}

