
#> mgs:v5.0.0/actionbar/add_icon_ammo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show
#

# Build icons recursively
scoreboard players set #i mgs.data 0
execute if score #i mgs.data < #capacity mgs.data run function mgs:v5.0.0/actionbar/build_icon_loop

