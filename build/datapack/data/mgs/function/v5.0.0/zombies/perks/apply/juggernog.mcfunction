
#> mgs:v5.0.0/zombies/perks/apply/juggernog
#
# @within	???
#

# Increase max health to 40 HP
attribute @s minecraft:max_health base set 40
data modify entity @s Health set value 40f
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.juggernog_max_hp_40","color":"dark_red","bold":true}]

