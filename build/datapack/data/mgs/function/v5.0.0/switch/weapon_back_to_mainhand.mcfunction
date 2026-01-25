
#> mgs:v5.0.0/switch/weapon_back_to_mainhand
#
# @executed	as @n[type=item,distance=..3,nbt={...}]
#
# @within	mgs:v5.0.0/switch/reload_to_dropped_weapon [ as @n[type=item,distance=..3,nbt={...}] ]
#

# Move reloaded item back to player's mainhand
item replace entity @p[tag=mgs.to_reload] weapon.mainhand from entity @s contents
kill @s

