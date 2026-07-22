
#> mgs:v5.1.0/switch/fire_mode_on_dropped_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/switch/check_fire_mode_on_drop
#

# Find nearest dropped gun item and execute as it (only if mainhand is empty)
tag @s add mgs.to_pickup
execute unless items entity @s weapon.mainhand * as @n[type=item,distance=..3,nbt={Item:{components:{"minecraft:custom_data":{mgs:{gun:true}}}}}] run function mgs:v5.1.0/switch/weapon_back_to_mainhand
tag @s remove mgs.to_pickup

# Copy gun data (the weapon is back in the mainhand by now)
function mgs:v5.1.0/utils/copy_gun_data

# Skip weapons without a second mode (throwables carry a fire_mode but shouldn't toggle)
execute unless data storage mgs:gun all.stats.can_auto unless data storage mgs:gun all.stats.can_burst run return 0

# Cycle auto -> semi -> burst -> auto (narrowed to what the weapon supports)
function mgs:v5.1.0/switch/do_toggle_fire_mode

