
#> mgs:v5.4.2/players/read_name
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/players/append_self
#			mgs:v5.4.2/stats/login
#

execute at @s run summon armor_stand ~ ~ ~ {Tags:["mgs_name_probe"],Invisible:1b,NoGravity:1b}
loot replace entity @e[type=armor_stand,tag=mgs_name_probe,limit=1] armor.head loot mgs:get_username
data modify storage mgs:temp _name set from entity @e[type=armor_stand,tag=mgs_name_probe,limit=1] equipment.head.components."minecraft:profile".name
kill @e[type=armor_stand,tag=mgs_name_probe]

