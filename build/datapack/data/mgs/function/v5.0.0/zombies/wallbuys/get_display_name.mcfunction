
#> mgs:v5.0.0/zombies/wallbuys/get_display_name
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_right_click
#			mgs:v5.0.0/zombies/wallbuys/on_hover
#

# Default to localized display item name.
data modify storage mgs:temp _wb_display_name set from storage mgs:temp _wb_weapon.item_name

# If a custom map name is set, use it instead.
execute unless data storage mgs:temp _wb_weapon{name:""} if data storage mgs:temp _wb_weapon.name run data modify storage mgs:temp _wb_display_name set from storage mgs:temp _wb_weapon.name

