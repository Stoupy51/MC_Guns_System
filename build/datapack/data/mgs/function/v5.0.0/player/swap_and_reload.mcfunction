
#> mgs:v5.0.0/player/swap_and_reload
#
# @executed	as @a[sort=random] & at @s
#
# @within	mgs:v5.0.0/player/reload_check
#

# Move offhand item to mainhand
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand with air

# Copy gun data
function mgs:v5.0.0/utils/copy_gun_data

# Reload the weapon
function mgs:v5.0.0/ammo/reload

