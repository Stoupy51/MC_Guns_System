
#> mgs:v5.1.0/player/swap_and_reload
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/offhand_swap_check
#

# Move offhand item back to mainhand
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand with air

# Reload the weapon. Throwables carry {gun:true} but no reload_time, and ammo/reload would store
# a result from that missing field, leaving a garbage cooldown that locks the item.
function mgs:v5.1.0/utils/copy_gun_data
execute unless data storage mgs:gun all.stats.reload_time run return 0
function mgs:v5.1.0/ammo/reload

