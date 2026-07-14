
#> mgs:v5.1.0/zombies/bonus/max_ammo_grenades
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:zombies/bonus/max_ammo
#

# Has grenades: set the stack to full (4) and stop
execute if items entity @s hotbar.7 *[custom_data~{mgs:{gun:true}}] run return run item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4

# Empty slot (all grenades used): give a fresh frag, fill to 4, and re-tag the slot
execute unless items entity @s hotbar.7 * run loot replace entity @s hotbar.7 loot mgs:i/frag_grenade
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}

