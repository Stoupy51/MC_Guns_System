
#> mgs:v5.1.0/zombies/perks/pool/try_index/speed_cola
#
# @within	mgs:v5.1.0/zombies/perks/pool/choose_iter
#

scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_speed_cola mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.speed_cola matches 1 run scoreboard players set #pool_slot mgs.data 0
execute if score #pool_slot mgs.data matches 1 run scoreboard players set #pool_chosen mgs.data 1
execute if score #pool_slot mgs.data matches 1 run data modify storage mgs:temp _pool.perk_id set value "speed_cola"

