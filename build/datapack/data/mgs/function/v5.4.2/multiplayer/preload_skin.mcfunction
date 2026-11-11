
#> mgs:v5.4.2/multiplayer/preload_skin
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/end_prep [ at @s ]
#

summon minecraft:mannequin ~ ~ ~ {hide_description:true,Silent:true,NoGravity:true,Invulnerable:true,attributes:[{id:"minecraft:scale",base:0.05d}],Tags:["mgs.skin_preload","mgs.skin_new"]}
loot replace entity @n[type=minecraft:mannequin,tag=mgs.skin_new] weapon.mainhand loot mgs:get_username
data modify entity @n[type=minecraft:mannequin,tag=mgs.skin_new] profile set from entity @n[type=minecraft:mannequin,tag=mgs.skin_new] equipment.mainhand.components."minecraft:profile"
item replace entity @n[type=minecraft:mannequin,tag=mgs.skin_new] weapon.mainhand with minecraft:air
tag @n[type=minecraft:mannequin,tag=mgs.skin_new] remove mgs.skin_new

