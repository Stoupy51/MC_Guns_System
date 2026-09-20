
#> mgs:v5.1.0/zombies/inventory/replenish_grenades
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/start_round [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] ]
#

# Case 1: player already has grenades in slot 7 - add 2, cap at 4
execute if items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] run item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_add_2
execute if items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] store result score #nade_count mgs.data run data get entity @s Inventory[{Slot:7b}].count
execute if items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] if score #nade_count mgs.data matches 5.. run item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_4
execute if items entity @s hotbar.7 *[custom_data~{mgs:{gun:true,zombies:{hotbar:7}}}] run return 0

# Case 2: slot 7 is empty (used all grenades) - give 2 of the player's BOUGHT lethal type, not a
# hardcoded frag (a player who bought semtex and used them all should get 2 semtex back).
execute unless items entity @s hotbar.7 * run function mgs:v5.1.0/zombies/inventory/give_lethal_type {count:2}

