
#> mgs:v5.0.0/actionbar/add_icon_ammo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show
#

# Build icons recursively
scoreboard players set #i mgs.data 0
execute if score #i mgs.data < #capacity mgs.data run function mgs:v5.0.0/actionbar/build_icon_loop

# Append reserve ammo count after icons
data modify storage mgs:temp actionbar.list append value {"text":" | ","color":"#c77e36"}
execute store result score #reserve mgs.data run scoreboard players get @s mgs.reserve_ammo
data modify storage mgs:temp actionbar.list append value {"score":{"name":"#reserve","objective":"mgs.data"}}
data modify storage mgs:temp actionbar.list append value {"text":"x ","color":"gray"}
data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0],"color":"gray"}

