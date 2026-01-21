
#> mgs:v5.0.0/switch/toggle_fire_mode
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/check_fire_mode_toggle
#

# Find nearest dropped gun item and execute as it (only if mainhand is empty)
execute unless items entity @s weapon.mainhand * as @n[type=item,distance=..3,nbt={Item:{components:{"minecraft:custom_data":{mgs:{gun:true}}}}}] run function mgs:v5.0.0/switch/do_toggle

# Force weapon switch animation
function mgs:v5.0.0/switch/force_switch_animation

