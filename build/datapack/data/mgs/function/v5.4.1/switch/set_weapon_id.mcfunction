
#> mgs:v5.4.1/switch/set_weapon_id
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/switch/main
#

execute store result storage mgs:gun all.stats.weapon_id int 1 run scoreboard players add #next_id mgs.data 1
item modify entity @s weapon.mainhand mgs:v5.4.1/set_weapon_id

