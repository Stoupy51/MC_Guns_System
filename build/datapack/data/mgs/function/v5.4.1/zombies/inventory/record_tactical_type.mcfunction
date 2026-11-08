
#> mgs:v5.4.1/zombies/inventory/record_tactical_type
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/wallbuys/buy_tactical with storage mgs:temp _wb_weapon
#			mgs:v5.4.1/zombies/wallbuys/give_tactical {weapon_id:"$(weapon_id)"}
#
# @args		weapon_id (string)
#

scoreboard players set @s mgs.zb.tactical_type 0
$data modify storage mgs:temp _tactical_id set value "$(weapon_id)"
execute if data storage mgs:temp {_tactical_id:"smoke_grenade"} run scoreboard players set @s mgs.zb.tactical_type 1
execute if data storage mgs:temp {_tactical_id:"flash_grenade"} run scoreboard players set @s mgs.zb.tactical_type 2
execute if data storage mgs:temp {_tactical_id:"monkey_bomb"} run scoreboard players set @s mgs.zb.tactical_type 3

