
#> mgs:v5.0.0/multiplayer/marketplace/add_btn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/marketplace/prep_btn with storage mgs:temp _btn_data
#
# @args		name (unknown)
#			main_gun (unknown)
#			secondary_gun (unknown)
#			likes (unknown)
#			select_trig (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:{text:"$(name)",color:"green"},tooltip:{text:"Main: $(main_gun) | Secondary: $(secondary_gun)\nLikes: $(likes)\nClick to use this loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set $(select_trig)"}}

