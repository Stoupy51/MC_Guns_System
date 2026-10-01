
#> mgs:v5.1.0/ammo/inventory/has_ammo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/reload with storage mgs:gun all.stats
#			mgs:v5.1.0/ammo/single_reload_continue with storage mgs:gun all.stats
#
# @args		base_weapon (unknown)
#

# Check all slots for matching magazines with bullets (return 1 if found, fail otherwise)
# Excludes empty non-consumable magazines (remaining_bullets: 0)
# Consumable magazines don't have this field, so they pass the 'unless' check if they exist
$execute if items entity @s container.* *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s weapon.offhand *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.cursor *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.crafting.* *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1

return fail

