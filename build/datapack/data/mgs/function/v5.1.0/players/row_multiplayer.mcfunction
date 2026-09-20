
#> mgs:v5.1.0/players/row_multiplayer
#
# @within	???
#
# @args		name (unknown)
#			color (unknown)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"$(color)"},tooltip:{translate:"mgs.refresh_the_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_multiplayer"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.red",color:"red"},tooltip:{translate:"mgs.move_to_red_team"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_to_red"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.blue",color:"blue"},tooltip:{translate:"mgs.move_to_blue_team"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_to_blue"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_remove"}}

