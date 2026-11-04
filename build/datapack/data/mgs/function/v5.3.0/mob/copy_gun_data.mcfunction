
#> mgs:v5.3.0/mob/copy_gun_data
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/mob/tick
#

data remove storage mgs:gun all
data modify storage mgs:gun all set from entity @s equipment.mainhand.components."minecraft:custom_data".mgs

