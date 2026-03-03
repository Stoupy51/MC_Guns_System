
#> mgs:v5.0.0/multiplayer/my_loadouts/add_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/my_loadouts/prep_btn with storage mgs:temp _btn_data
#
# @args		name (unknown)
#			main_gun (unknown)
#			secondary_gun (unknown)
#			select_trig (unknown)
#			delete_trig (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"green"},tooltip:{text:"Main: $(main_gun) | Secondary: $(secondary_gun)\nClick to use this loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set $(select_trig)"}}
$data modify storage mgs:temp dialog.actions append value {label:{translate: "mgs.delete",color:"red"},tooltip:{text:"Delete: $(name)"},action:{type:"run_command",command:"/trigger mgs.player.config set $(delete_trig)"}}

