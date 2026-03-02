
#> mgs:v5.0.0/mob/copy_gun_data
#
# @executed	as @e[tag=mgs.armed] & at @s
#
# @within	mgs:v5.0.0/mob/tick
#

# Copy gun data from equipment mainhand
data remove storage mgs:gun all
data modify storage mgs:gun all set from entity @s equipment.mainhand.components."minecraft:custom_data".mgs

