
#> mgs:v5.4.0/ammo/compute_reserve
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/switch/on_weapon_switch
#			mgs:v5.4.0/ammo/inventory/find
#			mgs:zombies/bonus/max_ammo
#			mgs:v5.4.0/zombies/pap/on_right_click
#			mgs:v5.4.0/zombies/pap/anim/collect_give [ as @p[tag=mgs.pap_owner] ]
#			mgs:v5.4.0/zombies/pap/upgrade_core
#			mgs:v5.4.0/zombies/wallbuys/on_right_click
#			mgs:v5.4.0/multiplayer/perks/scavenger_refill
#

execute unless data storage mgs:gun all.gun run return fail

# Grenades have no base_weapon.
execute unless data storage mgs:gun all.stats.base_weapon run return fail

scoreboard players set @s mgs.reserve_ammo 0

# Run as the ticking player.
function mgs:v5.4.0/ammo/reserve/scan with storage mgs:gun all.stats
return 0

