
#> mgs:v5.0.0/multiplayer/my_loadouts/add_btn_public
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/prep_btn with storage mgs:temp _btn_data
#
# @args		name (unknown)
#			main_gun_display (unknown)
#			primary_mag_count (unknown)
#			secondary_gun_display (unknown)
#			secondary_mag_count (unknown)
#			equip_slot1_name (unknown)
#			equip_slot2_name (unknown)
#			points_used (unknown)
#			perks_count (unknown)
#			perk0 (unknown)
#			perk1 (unknown)
#			perk2 (unknown)
#			likes (unknown)
#			favorites_count (unknown)
#			select_trig (unknown)
#			vis_trig (unknown)
#			delete_trig (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"green"},tooltip:["",{"text":"$(main_gun_display)","color":"green"},{"text":" x$(primary_mag_count) mags","color":"dark_green"},"\n",{"text":"$(secondary_gun_display)","color":"yellow"},{"text":" x$(secondary_mag_count) mags","color":"gold"},"\n",[{"text":"","color":"gray"},{"translate": "mgs.grenades"},": "],{"text":"$(equip_slot1_name)","color":"aqua"},{"text":" + $(equip_slot2_name)","color":"aqua"},"\n",[{"text":"","color":"white"},{"text":"Points"},": "],{"text":"$(points_used)/10pts","color":"gold"},[{"text":"","color":"white"},"  ",{"translate": "mgs.perks"},": "],{"text":"$(perks_count)","color":"light_purple"},{"text":"$(perk0)$(perk1)$(perk2)","color":"light_purple"},"\n",{"text":"\u2665 $(likes) likes","color":"red"},{"text":"  \u2b50 $(favorites_count) favs","color":"yellow"},"\n",{"translate": "mgs.public","color":"green","italic":true},"\n\n",{"text":"\u25b6 Click to select","color":"dark_gray","italic":true}],action:{type:"run_command",command:"/trigger mgs.player.config set $(select_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.public_private",color:"dark_aqua"},tooltip:{translate: "mgs.toggle_this_loadout_to_private",color:"red"},action:{type:"run_command",command:"/trigger mgs.player.config set $(vis_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:[{text:"",color:"red"},"🗑 ",{translate: "mgs.delete"}],tooltip:{translate: "mgs.permanently_delete_this_loadout",color:"dark_red"},action:{type:"run_command",command:"/trigger mgs.player.config set $(delete_trig)"}}

