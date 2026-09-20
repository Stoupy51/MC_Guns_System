
#> mgs:v5.1.0/zombies/inventory/record_lethal_type
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/buy_lethal
#

scoreboard players set @s mgs.zb.lethal_type 0
execute if data storage mgs:temp _wb_weapon{weapon_id:"semtex"} run scoreboard players set @s mgs.zb.lethal_type 1
execute if data storage mgs:temp _wb_weapon{weapon_id:"smoke_grenade"} run scoreboard players set @s mgs.zb.lethal_type 2
execute if data storage mgs:temp _wb_weapon{weapon_id:"flash_grenade"} run scoreboard players set @s mgs.zb.lethal_type 3

