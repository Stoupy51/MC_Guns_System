
#> mgs:v5.4.2/player/swap_and_reload
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/offhand_swap_check
#

item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand with air

# Throwables carry {gun:true} but no reload_time: ammo/reload would store a garbage cooldown from it and lock the item.
function mgs:v5.4.2/utils/copy_gun_data
execute unless data storage mgs:gun all.stats.reload_time run return 0
function mgs:v5.4.2/ammo/reload

