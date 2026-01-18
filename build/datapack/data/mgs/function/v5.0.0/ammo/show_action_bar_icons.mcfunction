
#> mgs:v5.0.0/ammo/show_action_bar_icons
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/ammo/show_action_bar
#

# Start building
scoreboard players set #i mgs.data 0
execute if score #i mgs.data < #capacity mgs.data run function mgs:v5.0.0/ammo/build_actionbar

# Show actionbar
function mgs:v5.0.0/ammo/display_actionbar with storage mgs:temp actionbar

