
#> mgs:v5.0.0/multiplayer/build_class_btn
#
# @within	mgs:v5.0.0/multiplayer/build_class_btn with storage mgs:temp class_iter[0]
#			mgs:v5.0.0/multiplayer/select_class with storage mgs:temp class_iter[0]
#
# @args		name (unknown)
#			lore (unknown)
#			main_gun (unknown)
#			secondary_gun (unknown)
#			trigger_value (unknown)
#

# Build tooltip from current class
$data modify storage mgs:temp _btn set value {label:{text:"$(name)",color:"green"},tooltip:{text:"$(lore)\nMain: $(main_gun)\nSecondary: $(secondary_gun)"},action:{type:"run_command",command:"/trigger mgs.player.config set $(trigger_value)"}}

# Append to dialog actions
data modify storage mgs:temp dialog.actions append from storage mgs:temp _btn

# Remove processed class and recurse
data remove storage mgs:temp class_iter[0]
execute if data storage mgs:temp class_iter[0] run function mgs:v5.0.0/multiplayer/build_class_btn with storage mgs:temp class_iter[0]

