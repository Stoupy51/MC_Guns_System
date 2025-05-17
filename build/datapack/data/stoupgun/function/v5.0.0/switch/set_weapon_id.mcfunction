
#> stoupgun:v5.0.0/switch/set_weapon_id
#
# @within	stoupgun:v5.0.0/switch/main
#

execute store result storage stoupgun:gun stats.weapon_id int 1 run scoreboard players add #next_id stoupgun.data 1
item modify entity @s weapon.mainhand stoupgun:v5.0.0/set_weapon_id

