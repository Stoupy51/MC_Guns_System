
#> mgs:v5.3.0/players/row_editor
#
# @within	mgs:v5.3.0/players/list_entry {id:$(id),name:"$(name)",color:"$(color)"}
#
# @args		name (string)
#			color (string)
#			id (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"$(color)"},tooltip:{translate:"mgs.refresh_the_list",fallback:"Refresh the list"},action:{type:"run_command",command:"/function mgs:v5.3.0/players/list_editor"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate:"mgs.invite",fallback:"Invite",color:"aqua"},tooltip:{translate:"mgs.bring_into_this_editor_session",fallback:"Bring into this editor session"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.3.0/players/editor_invite"}}

