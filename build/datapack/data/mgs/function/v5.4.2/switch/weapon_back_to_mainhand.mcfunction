
#> mgs:v5.4.2/switch/weapon_back_to_mainhand
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/switch/fire_mode_on_dropped_weapon [ as @n[type=item,distance=..3,nbt={...}] ]
#

item replace entity @p[tag=mgs.to_pickup] weapon.mainhand from entity @s contents
kill @s

