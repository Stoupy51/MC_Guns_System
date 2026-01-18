
#> mgs:v5.0.0/switch/set_weapon_id
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/main
#

execute store result storage mgs:gun all.stats.weapon_id int 1 run scoreboard players add #next_id mgs.data 1
item modify entity @s weapon.mainhand mgs:v5.0.0/set_weapon_id

