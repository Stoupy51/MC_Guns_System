
#> mgs:v5.1.0/zombies/perks/pool/try_index
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"juggernog"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"speed_cola"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"double_tap"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"quick_revive"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"mule_kick"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"stamin_up"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"phd_flopper"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"deadshot"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"timeslip"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"electric_cherry"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"tombstone"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"whos_who"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"dying_wish"}
#			mgs:v5.1.0/zombies/perks/pool/choose_iter {perk_id:"widows_wine"}
#
# @args		perk_id (string)
#

scoreboard players set #pool_slot mgs.data 0
$execute if score #map_perk_$(perk_id) mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
$execute if score @n[tag=mgs.pool_target] mgs.zb.perk.$(perk_id) matches 1 run scoreboard players set #pool_slot mgs.data 0
execute if score #pool_slot mgs.data matches 1 run scoreboard players operation #pool_chosen mgs.data = #pool_roll mgs.data
$execute if score #pool_slot mgs.data matches 1 run data modify storage mgs:temp _pool.perk_id set value "$(perk_id)"

