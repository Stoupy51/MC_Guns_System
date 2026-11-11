
#> mgs:v5.4.2/zombies/wallbuys/get_display_name
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/wallbuys/on_right_click
#			mgs:v5.4.2/zombies/wallbuys/on_hover
#

data modify storage mgs:temp _wb_display_name set from storage mgs:temp _wb_weapon.item_name

# A custom map name wins.
execute unless data storage mgs:temp _wb_weapon{name:""} if data storage mgs:temp _wb_weapon.name run data modify storage mgs:temp _wb_display_name set from storage mgs:temp _wb_weapon.name

