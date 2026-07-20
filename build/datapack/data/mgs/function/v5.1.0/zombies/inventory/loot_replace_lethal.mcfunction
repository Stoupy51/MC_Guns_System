
#> mgs:v5.1.0/zombies/inventory/loot_replace_lethal
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/give_lethal_type
#			mgs:v5.1.0/zombies/inventory/recreate_critical_items
#

execute unless score @s mgs.zb.lethal_type matches 1.. run loot replace entity @s hotbar.7 loot mgs:i/frag_grenade
execute if score @s mgs.zb.lethal_type matches 1 run loot replace entity @s hotbar.7 loot mgs:i/semtex
execute if score @s mgs.zb.lethal_type matches 2 run loot replace entity @s hotbar.7 loot mgs:i/smoke_grenade
execute if score @s mgs.zb.lethal_type matches 3 run loot replace entity @s hotbar.7 loot mgs:i/flash_grenade

