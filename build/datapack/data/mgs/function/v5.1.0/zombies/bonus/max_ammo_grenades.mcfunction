
#> mgs:v5.1.0/zombies/bonus/max_ammo_grenades
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:zombies/bonus/max_ammo
#

# Tactical slot (hotbar.6: monkey bombs, smoke, flash): back to 3, or 3 of the last bought type once emptied.
execute if items entity @s hotbar.6 *[custom_data~{mgs:{gun:true}}] run item modify entity @s hotbar.6 mgs:v5.1.0/grenade/set_count_3
execute unless items entity @s hotbar.6 * if score @s mgs.zb.tactical_type matches 1.. run function mgs:v5.1.0/zombies/inventory/give_tactical_type

# Lethal slot (hotbar.7): back to 4.
execute if items entity @s hotbar.7 *[custom_data~{mgs:{gun:true}}] run return run item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4

# Empty lethal slot: 4 of the bought lethal type (semtex stays semtex); give_lethal_type re-tags the slot.
execute unless items entity @s hotbar.7 * run function mgs:v5.1.0/zombies/inventory/give_lethal_type {count:4}

