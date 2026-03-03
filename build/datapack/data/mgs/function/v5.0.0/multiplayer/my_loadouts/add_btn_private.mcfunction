
#> mgs:v5.0.0/multiplayer/my_loadouts/add_btn_private
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/prep_btn with storage mgs:temp _btn_data
#
# @args		name (unknown)
#			main_gun (unknown)
#			secondary_gun (unknown)
#			select_trig (unknown)
#			vis_trig (unknown)
#			delete_trig (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"red"},tooltip:["",{text:"$(main_gun)",color:"green"},{text:" + ",color:"gray"},{text:"$(secondary_gun)",color:"yellow"},"\n",{translate: "mgs.private",color:"red",italic:true},"\n\n",{translate: "mgs.click_to_select",color:"dark_gray",italic:true}],action:{type:"run_command",command:"/trigger mgs.player.config set $(select_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:{text:"👁",color:"gray"},width:20,tooltip:["",{translate: "mgs.toggle_to",color:"white"},{translate: "mgs.public",color:"green"}],action:{type:"run_command",command:"/trigger mgs.player.config set $(vis_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:{text:"🗑",color:"red"},width:20,tooltip:{translate: "mgs.delete_this_loadout",color:"red"},action:{type:"run_command",command:"/trigger mgs.player.config set $(delete_trig)"}}

