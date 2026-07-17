
#> mgs:v5.1.0/utils/copy_gun_data
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#			mgs:v5.1.0/player/set_pending_clicks
#			mgs:v5.1.0/switch/reload_to_dropped_weapon
#			mgs:v5.1.0/switch/do_toggle_fire_mode
#			mgs:zombies/bonus/max_ammo
#			mgs:v5.1.0/zombies/wallbuys/on_right_click
#

# Copy gun data
data remove storage mgs:gun all
data modify storage mgs:gun SelectedItem set value {id:""}
execute unless items entity @s weapon.mainhand *[custom_data~{mgs:{}}] run return 0
data modify storage mgs:gun SelectedItem set from entity @s SelectedItem
data modify storage mgs:gun all set from storage mgs:gun SelectedItem.components."minecraft:custom_data".mgs

