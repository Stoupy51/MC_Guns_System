
#> mgs:v5.1.0/zombies/bonus/max_ammo_grenades
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:zombies/bonus/max_ammo
#

# Tactical slot (hotbar.6, e.g. Monkey Bombs): top back to 3 — refill only, never granted from
# an empty slot (tacticals come exclusively from the Mystery Box or a wall-buy)
execute if items entity @s hotbar.6 *[custom_data~{mgs:{gun:true}}] run item modify entity @s hotbar.6 mgs:v5.1.0/grenade/set_count_3

# Has grenades: set the stack to full (4) and stop
execute if items entity @s hotbar.7 *[custom_data~{mgs:{gun:true}}] run return run item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4

# Empty slot (all grenades used): give 4 of the player's BOUGHT lethal type (semtex stays semtex),
# not a hardcoded frag; give_lethal_type re-tags the slot too.
execute unless items entity @s hotbar.7 * run function mgs:v5.1.0/zombies/inventory/give_lethal_type {count:4}

