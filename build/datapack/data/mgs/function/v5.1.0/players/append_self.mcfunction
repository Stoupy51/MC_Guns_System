
#> mgs:v5.1.0/players/append_self
#
# @executed	as @a
#
# @within	mgs:v5.1.0/players/list_multiplayer [ as @a ]
#			mgs:v5.1.0/players/list_zombies [ as @a ]
#			mgs:v5.1.0/players/list_missions [ as @a ]
#

data modify storage mgs:temp _plr_entry set value {color:"gray",name:"???"}
execute store result storage mgs:temp _plr_entry.id int 1 run scoreboard players get @s bs.id
execute if data storage mgs:temp {_plr_mode:"multiplayer"} if score @s mgs.mp.team matches 1 run data modify storage mgs:temp _plr_entry.color set value "red"
execute if data storage mgs:temp {_plr_mode:"multiplayer"} if score @s mgs.mp.team matches 2 run data modify storage mgs:temp _plr_entry.color set value "blue"
execute if data storage mgs:temp {_plr_mode:"zombies"} if score @s mgs.zb.in_game matches 1 run data modify storage mgs:temp _plr_entry.color set value "green"
execute if data storage mgs:temp {_plr_mode:"missions"} if score @s mgs.mi.in_game matches 1 run data modify storage mgs:temp _plr_entry.color set value "green"

# Resolve the real username: fill an invisible probe's head with @s's profile ("this" in the loot
# table), then read the name out of its profile component (dual path covers both equipment NBT formats).
execute at @s run summon armor_stand ~ ~ ~ {Tags:["mgs_name_probe"],Invisible:1b,NoGravity:1b}
loot replace entity @e[type=armor_stand,tag=mgs_name_probe,limit=1] armor.head loot mgs:players/name_head
data modify storage mgs:temp _plr_entry.name set from entity @e[type=armor_stand,tag=mgs_name_probe,limit=1] ArmorItems[3].components."minecraft:profile".name
data modify storage mgs:temp _plr_entry.name set from entity @e[type=armor_stand,tag=mgs_name_probe,limit=1] equipment.head.components."minecraft:profile".name
kill @e[type=armor_stand,tag=mgs_name_probe]

data modify storage mgs:temp _plr_iter append from storage mgs:temp _plr_entry

