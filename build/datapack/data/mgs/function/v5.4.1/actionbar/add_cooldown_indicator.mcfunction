
#> mgs:v5.4.1/actionbar/add_cooldown_indicator
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/actionbar/show
#

execute if score @s mgs.cooldown <= #total_tick mgs.data run data modify storage mgs:temp actionbar.list append value {"text":" ● ","color":"green"}
execute if score @s mgs.cooldown > #total_tick mgs.data run data modify storage mgs:temp actionbar.list append value {"text":" ● ","color":"dark_red"}

