
#> mgs:v5.2.0/zombies/inventory/give_tactical_type
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.2.0/zombies/bonus/max_ammo_grenades
#

execute if score @s mgs.zb.tactical_type matches 1 run loot replace entity @s hotbar.6 loot mgs:i/smoke_grenade
execute if score @s mgs.zb.tactical_type matches 2 run loot replace entity @s hotbar.6 loot mgs:i/flash_grenade
execute if score @s mgs.zb.tactical_type matches 3 run loot replace entity @s hotbar.6 loot mgs:i/monkey_bomb
item modify entity @s hotbar.6 mgs:v5.2.0/grenade/set_count_3
function mgs:v5.2.0/zombies/inventory/apply_slot_tag {slot:"hotbar.6",group:"hotbar",index:6}

