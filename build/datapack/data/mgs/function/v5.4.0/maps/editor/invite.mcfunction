
#> mgs:v5.4.0/maps/editor/invite
#
# @within	mgs:v5.4.0/dialog/close_then
#			string in mgs:v5.4.0/maps/editor/enter
#

execute unless score @s mgs.mp.map_edit matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_must_be_in_map_editor_to_invite_players","fallback":"You must be in map editor to invite players.","color":"red"}]

data modify storage mgs:temp _plr_mode set value "editor"
data modify storage mgs:temp _plr_iter set value []
execute as @a unless score @s mgs.mp.map_edit matches 1 run function mgs:v5.4.0/players/append_self

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:["","👥 ",{translate:"mgs.invite_to_the_editor",fallback:"Invite to the Editor",color:"aqua",bold:true}],body:[{type:"minecraft:plain_message",contents:{translate:"mgs.check_the_players_to_invite",fallback:"Check the players to invite.",color:"gray"}}],inputs:[],actions:[{label:{translate:"mgs.invite",fallback:"Invite",color:"green"},action:{type:"minecraft:dynamic/run_command",template:""}},{label:{translate:"mgs.everyone",fallback:"Everyone",color:"aqua"},tooltip:{translate:"mgs.invite_every_online_player",fallback:"Invite every online player"},action:{type:"run_command",command:"/function mgs:v5.4.0/maps/editor/invite_all"}}],columns:2,exit_action:{label:{translate:"mgs.close",fallback:"Close",color:"gray"}}}
execute unless data storage mgs:temp _plr_iter[0] run data modify storage mgs:temp dialog.body[0].contents set value {translate:"mgs.everyone_online_already_edits_this_map",fallback:"Everyone online already edits this map.",color:"gray"}

# A dialog refuses a template without variables, so Invite goes when there is no box.
execute unless data storage mgs:temp _plr_iter[0] run data remove storage mgs:temp dialog.actions[0]

# The Invite template lists every box, as `ids:[$(p12),$(p7),0]`: a box gives its player's bs.id when checked, else 0. `d` holds the "$" a macro cannot write itself.
data modify storage mgs:temp _inv set value {tpl:"",d:"$"}
execute if data storage mgs:temp _plr_iter[0] run function mgs:v5.4.0/maps/editor/invite_box
execute unless data storage mgs:temp _inv{tpl:""} run function mgs:v5.4.0/maps/editor/invite_template with storage mgs:temp _inv
function mgs:v5.4.0/multiplayer/show_dialog with storage mgs:temp

