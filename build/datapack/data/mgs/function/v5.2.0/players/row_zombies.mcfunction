
#> mgs:v5.2.0/players/row_zombies
#
# @within	mgs:v5.2.0/players/list_entry {id:$(id),name:"$(name)",color:"$(color)"}
#
# @args		name (string)
#			color (string)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"$(color)"},tooltip:{translate:"mgs.refresh_the_list",fallback:"Refresh the list"},action:{type:"run_command",command:"/function mgs:v5.2.0/players/list_zombies"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.join",fallback:"Join",color:"green"},tooltip:{translate:"mgs.add_to_the_zombies_game",fallback:"Add to the zombies game"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.2.0/players/zb_join"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.remove",fallback:"Remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator",fallback:"Remove from the game (spectator)"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.2.0/players/zb_remove"}}

