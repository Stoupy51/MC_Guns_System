
#> mgs:v5.0.0/ammo/build_actionbar
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/show_action_bar_icons
#			mgs:v5.0.0/ammo/build_actionbar
#

# Append bullet icon
data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0]}

# For empty bullets, use outline
execute if score #i mgs.data >= #remaining mgs.data run data modify storage mgs:temp actionbar.list[-1].text set value "B"

# Increment i
scoreboard players add #i mgs.data 1

# Recurse if not done
execute if score #i mgs.data < #capacity mgs.data run function mgs:v5.0.0/ammo/build_actionbar

