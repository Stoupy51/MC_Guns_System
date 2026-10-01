
#> mgs:v5.1.0/ammo/inventory/has_ammo
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/ammo/reload with storage mgs:gun all.stats
#			mgs:v5.1.0/ammo/single_reload_continue with storage mgs:gun all.stats
#
# @args		base_weapon (unknown)
#

# Returns 1 when found. Empty regular magazines (remaining_bullets 0) are skipped; consumables have no such field.
$execute if items entity @s container.* *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s weapon.offhand *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.cursor *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1
$execute if items entity @s player.crafting.* *[custom_data~{mgs:{magazine:true,weapon:"$(base_weapon)"}},!custom_data~{mgs:{stats:{remaining_bullets:0}}}] run return 1

return fail

