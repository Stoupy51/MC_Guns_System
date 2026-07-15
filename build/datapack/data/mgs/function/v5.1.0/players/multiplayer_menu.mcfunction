
#> mgs:v5.1.0/players/multiplayer_menu
#
# @within	???
#
# @args		name (unknown)
#			id (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{text:"$(name)",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate:"mgs.assign_this_player_to_a_team",color:"gray"}}],columns:3,pause:false,after_action:"none",actions:[{label:{translate:"mgs.red",color:"red"},tooltip:{translate:"mgs.move_to_red_team"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_to_red"}},{label:{translate:"mgs.blue",color:"blue"},tooltip:{translate:"mgs.move_to_blue_team"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_to_blue"}},{label:{translate:"mgs.remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/mp_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_multiplayer"}}}
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

