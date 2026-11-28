
#> mgs:v5.4.4/lobby/menu_buttons
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/player/config/menu
#

execute unless score @s mgs.lobby.queue matches 1 run data modify storage mgs:temp dialog.actions append value {label:["","⚔ ",{translate:"mgs.play_multiplayer",fallback:"Play Multiplayer",color:"red",bold:true}],tooltip:{translate:"mgs.join_the_multiplayer_queue_vote_then_play",fallback:"Join the Multiplayer queue, vote, then play"},action:{type:"run_command",command:"/trigger mgs.player.config set 1651"}}
execute unless score @s mgs.lobby.queue matches 2 run data modify storage mgs:temp dialog.actions append value {label:["","🧟 ",{translate:"mgs.play_zombies",fallback:"Play Zombies",color:"dark_green",bold:true}],tooltip:{translate:"mgs.join_the_zombies_queue_vote_then_play",fallback:"Join the Zombies queue, vote, then play"},action:{type:"run_command",command:"/trigger mgs.player.config set 1652"}}
execute unless score @s mgs.lobby.queue matches 3 run data modify storage mgs:temp dialog.actions append value {label:["","🎯 ",{translate:"mgs.play_missions",fallback:"Play Missions",color:"gold",bold:true}],tooltip:{translate:"mgs.join_the_missions_queue_vote_then_play",fallback:"Join the Missions queue, vote, then play"},action:{type:"run_command",command:"/trigger mgs.player.config set 1653"}}
data modify storage mgs:temp dialog.actions append value {label:["","🏠 ",{translate:"mgs.back_to_lobby",fallback:"Back to Lobby",color:"yellow",bold:true}],tooltip:{translate:"mgs.leave_your_queue_and_your_game",fallback:"Leave your queue and your game"},action:{type:"run_command",command:"/trigger mgs.player.config set 1650"}}

