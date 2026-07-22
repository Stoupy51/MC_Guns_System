
#> mgs:v5.1.0/switch/weapon_back_to_mainhand
#
# @executed	as @n[type=item,distance=..3,nbt={...}]
#
# @within	mgs:v5.1.0/switch/fire_mode_on_dropped_weapon [ as @n[type=item,distance=..3,nbt={...}] ]
#

# Move the dropped item back to player's mainhand
item replace entity @p[tag=mgs.to_pickup] weapon.mainhand from entity @s contents
kill @s

