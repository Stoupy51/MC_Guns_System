
#> mgs:v5.0.0/multiplayer/marketplace/add_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/marketplace/prep_btn with storage mgs:temp _btn_data
#
# @args		name (unknown)
#			main_gun (unknown)
#			secondary_gun (unknown)
#			owner_name (unknown)
#			likes (unknown)
#			select_trig (unknown)
#			like_trig (unknown)
#			fav_trig (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"green"},tooltip:["",{text:"$(main_gun)",color:"green"},{text:" + ",color:"gray"},{text:"$(secondary_gun)",color:"yellow"},"\n",{text:"by $(owner_name)",color:"aqua",italic:true},"\n",{text:"♥ $(likes) likes",color:"red"},"\n\n",{translate: "mgs.click_to_select",color:"dark_gray",italic:true}],action:{type:"run_command",command:"/trigger mgs.player.config set $(select_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:{text:"👍",color:"yellow"},width:20,tooltip:{translate: "mgs.like_this_loadout",color:"yellow"},action:{type:"run_command",command:"/trigger mgs.player.config set $(like_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:{text:"⭐",color:"gold"},width:20,tooltip:{translate: "mgs.add_to_favorites",color:"gold"},action:{type:"run_command",command:"/trigger mgs.player.config set $(fav_trig)"}}

