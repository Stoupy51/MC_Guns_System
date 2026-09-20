
#> mgs:v5.1.0/players/row_missions
#
# @within	???
#
# @args		name (unknown)
#			color (unknown)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"$(color)"},tooltip:{translate:"mgs.refresh_the_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_missions"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.join",color:"green"},tooltip:{translate:"mgs.add_to_the_mission"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mi_join"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mi_remove"}}

