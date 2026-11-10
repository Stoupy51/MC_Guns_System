
#> mgs:v5.4.1/multiplayer/death_animation
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/simulate_death [ at @s ]
#

summon minecraft:mannequin ~ ~ ~ {hide_description:true,Tags:["mgs.death_mannequin"]}
data modify entity @n[type=minecraft:mannequin,tag=mgs.death_mannequin] Rotation set from entity @s Rotation
data modify entity @n[type=minecraft:mannequin,tag=mgs.death_mannequin] equipment set from entity @s equipment

# The get_username loot table gives a player_head with the profile, for the skin.
loot replace entity @n[type=minecraft:mannequin,tag=mgs.death_mannequin] weapon.mainhand loot mgs:get_username
data modify entity @n[type=minecraft:mannequin,tag=mgs.death_mannequin] profile set from entity @n[type=minecraft:mannequin,tag=mgs.death_mannequin] equipment.mainhand.components."minecraft:profile"
item replace entity @n[type=minecraft:mannequin,tag=mgs.death_mannequin] weapon.mainhand from entity @s weapon.mainhand

kill @n[type=minecraft:mannequin,tag=mgs.death_mannequin]

