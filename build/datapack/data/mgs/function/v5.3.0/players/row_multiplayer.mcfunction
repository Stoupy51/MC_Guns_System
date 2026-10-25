
#> mgs:v5.3.0/players/row_multiplayer
#
# @within	mgs:v5.3.0/players/list_entry {id:$(id),name:"$(name)",color:"$(color)"}
#
# @args		name (string)
#			color (string)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"$(color)"},tooltip:{translate:"mgs.refresh_the_list",fallback:"Refresh the list"},action:{type:"run_command",command:"/function mgs:v5.3.0/players/list_multiplayer"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.red",fallback:"Red",color:"red"},tooltip:{translate:"mgs.move_to_red_team",fallback:"Move to Red team"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.3.0/players/mp_to_red"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.blue",fallback:"Blue",color:"blue"},tooltip:{translate:"mgs.move_to_blue_team",fallback:"Move to Blue team"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.3.0/players/mp_to_blue"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.remove",fallback:"Remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator",fallback:"Remove from the game (spectator)"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.3.0/players/mp_remove"}}

