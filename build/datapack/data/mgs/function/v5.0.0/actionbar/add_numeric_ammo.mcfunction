
#> mgs:v5.0.0/actionbar/add_numeric_ammo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show
#

data modify storage mgs:temp actionbar.list append value {"score":{"name":"#remaining","objective":"mgs.data"}}
data modify storage mgs:temp actionbar.list append value {"text":"x "}
data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0],"color":"white"}
data modify storage mgs:temp actionbar.list append value {"text":" / ","color":"#c77e36"}
data modify storage mgs:temp actionbar.list append value {"score":{"name":"#capacity","objective":"mgs.data"}}
data modify storage mgs:temp actionbar.list append value {"text":"x "}
data modify storage mgs:temp actionbar.list append value {"text":"A","font":"mgs:icons","shadow_color":[0,0,0,0],"color":"white"}

