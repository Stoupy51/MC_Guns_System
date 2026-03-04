
#> mgs:v5.0.0/multiplayer/build_class_btn
#
# @within	mgs:v5.0.0/multiplayer/build_class_btn with storage mgs:temp class_iter[0]
#			mgs:v5.0.0/multiplayer/select_class with storage mgs:temp class_iter[0]
#
# @args		name (unknown)
#			lore (unknown)
#			main_gun (unknown)
#			main_mag_count (unknown)
#			secondary_gun (unknown)
#			secondary_mag_count (unknown)
#			equip_display (unknown)
#			trigger_value (unknown)
#

# Build rich tooltip from current class data (includes mag counts and equipment)
$data modify storage mgs:temp _btn set value {label:{text:"$(name)",color:"green"},tooltip:["",{text:"$(lore)","color":"gray"},{"text":"\n"},{"text":"Primary: ","color":"white"},{"text":"$(main_gun)","color":"green"},{"text":" x$(main_mag_count) mags","color":"dark_green"},{"text":"\n"},{"translate": "mgs.secondary","color":"white"},{"text":"$(secondary_gun)","color":"yellow"},{"text":" x$(secondary_mag_count) mags","color":"gold"},{"text":"\n"},{"translate": "mgs.grenades","color":"white"},{"text":"$(equip_display)","color":"aqua"},"\n\n",{"translate": "mgs.click_to_select","color":"dark_gray","italic":true}],action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger_value)"}}

# Append to dialog actions
data modify storage mgs:temp dialog.actions append from storage mgs:temp _btn

# Remove processed class and recurse
data remove storage mgs:temp class_iter[0]
execute if data storage mgs:temp class_iter[0] run function mgs:v5.0.0/multiplayer/build_class_btn with storage mgs:temp class_iter[0]

