
#> mgs:v5.0.0/ammo/compute_reserve
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/switch/on_weapon_switch
#			mgs:v5.0.0/ammo/inventory/find
#			mgs:zombies/bonus/max_ammo
#			mgs:v5.0.0/zombies/pap/on_right_click
#			mgs:v5.0.0/zombies/pap/anim_collect_give [ as @p[tag=mgs.pap_owner] ]
#

# Skip if not holding a gun
execute unless data storage mgs:gun all.gun run return fail

# Reset reserve counter
scoreboard players set @s mgs.reserve_ammo 0

# Sum bullets from all matching magazine slots (runs as ticking player)
function mgs:v5.0.0/ammo/reserve/scan with storage mgs:gun all.stats
return 0

