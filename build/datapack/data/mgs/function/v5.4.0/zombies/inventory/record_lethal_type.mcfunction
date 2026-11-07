
#> mgs:v5.4.0/zombies/inventory/record_lethal_type
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/wallbuys/buy_lethal
#

scoreboard players set @s mgs.zb.lethal_type 0
execute if data storage mgs:temp _wb_weapon{weapon_id:"semtex"} run scoreboard players set @s mgs.zb.lethal_type 1

