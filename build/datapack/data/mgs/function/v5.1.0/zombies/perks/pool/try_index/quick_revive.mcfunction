
#> mgs:v5.1.0/zombies/perks/pool/try_index/quick_revive
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/perks/pool/choose_iter
#

scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_quick_revive mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.quick_revive matches 1 run scoreboard players set #pool_slot mgs.data 0
execute if score #pool_slot mgs.data matches 1 run scoreboard players set #pool_chosen mgs.data 3
execute if score #pool_slot mgs.data matches 1 run data modify storage mgs:temp _pool.perk_id set value "quick_revive"

