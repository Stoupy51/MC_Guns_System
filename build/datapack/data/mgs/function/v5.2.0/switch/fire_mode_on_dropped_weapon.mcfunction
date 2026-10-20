
#> mgs:v5.2.0/switch/fire_mode_on_dropped_weapon
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.2.0/switch/check_fire_mode_on_drop
#

# The nearest dropped gun, only if the main hand is empty.
tag @s add mgs.to_pickup
execute unless items entity @s weapon.mainhand * as @n[type=item,distance=..3,nbt={Item:{components:{"minecraft:custom_data":{mgs:{gun:true}}}}}] run function mgs:v5.2.0/switch/weapon_back_to_mainhand
tag @s remove mgs.to_pickup

# The weapon is back in the main hand; a single-mode weapon has nothing to cycle.
function mgs:v5.2.0/utils/copy_gun_data
execute unless data storage mgs:gun all.stats.fire_modes[1] run return 0
function mgs:v5.2.0/switch/do_toggle_fire_mode

