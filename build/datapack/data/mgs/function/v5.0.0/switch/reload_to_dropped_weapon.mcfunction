
#> mgs:v5.0.0/switch/reload_to_dropped_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/check_reload_on_drop
#

# Find nearest dropped gun item and execute as it (only if mainhand is empty)
tag @s add mgs.to_reload
execute unless items entity @s weapon.mainhand * as @n[type=item,distance=..3,nbt={Item:{components:{"minecraft:custom_data":{mgs:{gun:true}}}}}] run function mgs:v5.0.0/switch/weapon_back_to_mainhand
tag @s remove mgs.to_reload

# Copy gun data
function mgs:v5.0.0/utils/copy_gun_data

# Reload
function mgs:v5.0.0/ammo/reload

