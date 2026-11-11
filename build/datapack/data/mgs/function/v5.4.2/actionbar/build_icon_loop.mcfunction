
#> mgs:v5.4.2/actionbar/build_icon_loop
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/actionbar/add_icon_ammo
#			mgs:v5.4.2/actionbar/build_icon_loop
#

# Full by default.
data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0]}

# Empty bullets are outlines.
execute if score #i mgs.data >= #remaining mgs.data run data modify storage mgs:temp actionbar.list[-1] set value {"text":"B","font":"mgs:icons","color":"gray","shadow_color":[0,0,0,0]}

scoreboard players add #i mgs.data 1

execute if score #i mgs.data < #capacity mgs.data run function mgs:v5.4.2/actionbar/build_icon_loop

