
#> mgs:v5.0.0/multiplayer/marketplace/add_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/marketplace/prep_btn with storage mgs:temp _btn_data
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
#			likes (unknown)
#			favorites_count (unknown)
#			owner_name (unknown)
#			select_trig (unknown)
#			like_trig (unknown)
#			fav_trig (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"green"},tooltip:["",{"text":"$(main_gun_display)","color":"green"},{"text":" x$(primary_mag_count) mags","color":"dark_green"},"\n",{"translate": "mgs.secondary","color":"gray"},{"text":"$(secondary_gun_display)","color":"yellow"},{"text":" x$(secondary_mag_count) mags","color":"gold"},"\n",{"translate": "mgs.grenades","color":"gray"},{"text":"$(equip_slot1_name)","color":"aqua"},{"text":" + $(equip_slot2_name)","color":"aqua"},"\n",{"translate": "mgs.points","color":"white"},{"text":"$(points_used)/10pts","color":"gold"},{"translate": "mgs.perks","color":"white"},{"text":"$(perks_count)","color":"light_purple"},"\n",{"text":"\u2665 $(likes) likes","color":"red"},{"text":"  \u2b50 $(favorites_count) favs","color":"yellow"},"\n",{"text":"by $(owner_name)","color":"aqua","italic":true},"\n\n",{"text":"\u25b6 Click to select","color":"dark_gray","italic":true}],action:{type:"run_command",command:"/trigger mgs.player.config set $(select_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:[{text:"♥ ",color:"red"},{translate: "mgs.like",color:"yellow"}],tooltip:{translate: "mgs.like_this_loadout",color:"yellow"},action:{type:"run_command",command:"/trigger mgs.player.config set $(like_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:[{text:"⭐ ",color:"gold"},{translate: "mgs.fav",color:"yellow"}],tooltip:{translate: "mgs.add_to_favorites",color:"gold"},action:{type:"run_command",command:"/trigger mgs.player.config set $(fav_trig)"}}

