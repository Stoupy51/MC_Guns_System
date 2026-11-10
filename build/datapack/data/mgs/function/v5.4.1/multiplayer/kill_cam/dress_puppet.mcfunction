
#> mgs:v5.4.1/multiplayer/kill_cam/dress_puppet
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/init_puppet [ as @a ]
#

data modify entity @n[type=minecraft:mannequin,tag=mgs.kc_new] equipment set from entity @s equipment
loot replace entity @n[type=minecraft:mannequin,tag=mgs.kc_new] weapon.mainhand loot mgs:get_username
data modify entity @n[type=minecraft:mannequin,tag=mgs.kc_new] profile set from entity @n[type=minecraft:mannequin,tag=mgs.kc_new] equipment.mainhand.components."minecraft:profile"
item replace entity @n[type=minecraft:mannequin,tag=mgs.kc_new] weapon.mainhand from entity @s weapon.mainhand

