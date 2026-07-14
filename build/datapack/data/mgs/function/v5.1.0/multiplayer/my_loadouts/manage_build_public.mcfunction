
#> mgs:v5.1.0/multiplayer/my_loadouts/manage_build_public
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/my_loadouts/manage_prep with storage mgs:temp _btn_data
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
#			perk3 (unknown)
#			perk4 (unknown)
#			perk5 (unknown)
#			perk6 (unknown)
#			perk7 (unknown)
#			perk8 (unknown)
#			likes (unknown)
#			favorites_count (unknown)
#			select_trig (unknown)
#			edit_trig (unknown)
#			vis_trig (unknown)
#			default_trig (unknown)
#			delete_trig (unknown)
#

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{text:"$(name)",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",{"text":"$(main_gun_display)","color":"green"},{"text":" x$(primary_mag_count) mags","color":"dark_green"},"\n",{"text":"$(secondary_gun_display)","color":"yellow"},{"text":" x$(secondary_mag_count) mags","color":"gold"},"\n",[{"text":"","color":"gray"},{"translate":"mgs.grenades"},": "],{"text":"$(equip_slot1_name)","color":"aqua"},{"text":" + $(equip_slot2_name)","color":"aqua"},"\n",[{"text":"","color":"white"},{"translate":"mgs.points"},": "],{"text":"$(points_used)/10pts","color":"gold"},[{"text":"","color":"white"},"  ",{"translate":"mgs.perks"},": "],{"text":"$(perks_count)","color":"light_purple"},{"text":"$(perk0)$(perk1)$(perk2)$(perk3)$(perk4)$(perk5)$(perk6)$(perk7)$(perk8)","color":"light_purple"},"\n",{"text":"\u2665 $(likes) likes","color":"red"},{"text":"  \u2b50 $(favorites_count) favs","color":"yellow"},"\n",{"translate":"mgs.public","color":"green","italic":true}]}],actions:[{label:[{text:"",color:"green",bold:true},"▶ ",{translate:"mgs.use_this_loadout"}],tooltip:{translate:"mgs.equip_this_loadout_applies_on_next_spawn"},action:{type:"run_command",command:"/trigger mgs.player.config set $(select_trig)"}},{label:[{text:"",color:"gold"},"✏ ",{translate:"mgs.edit"}],tooltip:{translate:"mgs.re_open_the_loadout_editor_pre_filled_saving_overwrites_this_loa",color:"yellow"},action:{type:"run_command",command:"/trigger mgs.player.config set $(edit_trig)"}},{label:{translate:"mgs.public_private",color:"dark_aqua"},tooltip:{translate:"mgs.toggle_this_loadout_to_private"},action:{type:"run_command",command:"/trigger mgs.player.config set $(vis_trig)"}},{label:[{text:"",color:"yellow"},"⭐ ",{translate:"mgs.set_as_default"}],tooltip:{translate:"mgs.auto_equip_this_loadout_when_a_game_starts"},action:{type:"run_command",command:"/trigger mgs.player.config set $(default_trig)"}},{label:[{text:"",color:"red"},"🗑 ",{translate:"mgs.delete"}],tooltip:{translate:"mgs.permanently_delete_this_loadout",color:"dark_red"},action:{type:"run_command",command:"/trigger mgs.player.config set $(delete_trig)"}}],columns:1,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 102"}}}
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

