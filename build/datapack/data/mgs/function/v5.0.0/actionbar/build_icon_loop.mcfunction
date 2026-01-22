
#> mgs:v5.0.0/actionbar/build_icon_loop
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/add_icon_ammo
#			mgs:v5.0.0/actionbar/build_icon_loop
#

# Append bullet icon (full by default)
data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0]}

# For empty bullets, use outline
execute if score #i mgs.data >= #remaining mgs.data run data modify storage mgs:temp actionbar.list[-1] set value {"text":"B","font":"mgs:icons","color":"gray","shadow_color":[0,0,0,0]}

# Increment counter
scoreboard players add #i mgs.data 1

# Recurse if not done
execute if score #i mgs.data < #capacity mgs.data run function mgs:v5.0.0/actionbar/build_icon_loop

