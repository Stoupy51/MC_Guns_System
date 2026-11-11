
#> mgs:v5.4.2/multiplayer/death_animation
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/simulate_death [ at @s ]
#

summon minecraft:mannequin ~ ~ ~ {hide_description:true,Tags:["mgs.death_mannequin","mgs.kc_new"]}
data modify entity @n[type=minecraft:mannequin,tag=mgs.death_mannequin] Rotation set from entity @s Rotation
function mgs:v5.4.2/multiplayer/kill_cam/dress_puppet

kill @n[type=minecraft:mannequin,tag=mgs.death_mannequin]

