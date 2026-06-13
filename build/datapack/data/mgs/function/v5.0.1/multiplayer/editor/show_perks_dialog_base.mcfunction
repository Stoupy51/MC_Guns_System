
#> mgs:v5.0.1/multiplayer/editor/show_perks_dialog_base
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/show_perks_dialog with storage mgs:temp
#
# @args		_pts (unknown)
#			_perk_count (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.loadout_perks",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_remaining"},": "],{"text":"$(_pts)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]},{type:"minecraft:plain_message",contents:{text:"Toggle perks below (max 3, 1 pt each). Selected: $(_perk_count)/3",color:"gray"}}],actions:[],columns:2,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 103"}}}

