
#> mgs:v5.3.0/players/read_name
#
# @executed	as @a
#
# @within	mgs:v5.3.0/players/append_self
#			mgs:v5.3.0/stats/login
#

execute at @s run summon armor_stand ~ ~ ~ {Tags:["mgs_name_probe"],Invisible:1b,NoGravity:1b}
loot replace entity @e[type=armor_stand,tag=mgs_name_probe,limit=1] armor.head loot mgs:get_username
data modify storage mgs:temp _name set from entity @e[type=armor_stand,tag=mgs_name_probe,limit=1] equipment.head.components."minecraft:profile".name
kill @e[type=armor_stand,tag=mgs_name_probe]

