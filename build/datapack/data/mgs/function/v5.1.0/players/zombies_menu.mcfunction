
#> mgs:v5.1.0/players/zombies_menu
#
# @within	???
#
# @args		name (unknown)
#			id (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{text:"$(name)",color:"dark_green",bold:true},body:[{type:"minecraft:plain_message",contents:{translate:"mgs.manage_this_player",color:"gray"}}],columns:2,pause:false,after_action:"none",actions:[{label:{translate:"mgs.join",color:"green"},tooltip:{translate:"mgs.add_to_the_zombies_game"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/zb_join"}},{label:{translate:"mgs.remove",color:"gray"},tooltip:{translate:"mgs.remove_from_the_game_spectator"},action:{type:"run_command",command:"/execute as @a[scores={bs.id=$(id)}] run function mgs:v5.1.0/players/zb_remove"}}],exit_action:{label:[{text:"◀ ",color:"gray"}, {translate:"mgs.back"}],tooltip:{translate:"mgs.back_to_player_list"},action:{type:"run_command",command:"/function mgs:v5.1.0/players/list_zombies"}}}
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

