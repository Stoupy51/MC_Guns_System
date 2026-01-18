
#> mgs:v5.0.0/utils/copy_gun_data
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#			mgs:v5.0.0/player/swap_and_reload
#

# Copy gun data
data remove storage mgs:gun all
data modify storage mgs:gun SelectedItem set value {id:""}
data modify storage mgs:gun SelectedItem set from entity @s SelectedItem
data modify storage mgs:gun all set from storage mgs:gun SelectedItem.components."minecraft:custom_data".mgs

