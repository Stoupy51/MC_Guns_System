
#> mgs:v5.1.0/zombies/perks/pool/count
#
# @within	mgs:v5.1.0/zombies/perks/pool/choose
#

scoreboard players set #pool_avail mgs.data 0
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_juggernog mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.juggernog matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_speed_cola mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.speed_cola matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_double_tap mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.double_tap matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_quick_revive mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.quick_revive matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_mule_kick mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.mule_kick matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_stamin_up mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.stamin_up matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_phd_flopper mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.phd_flopper matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_deadshot mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.deadshot matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_timeslip mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.timeslip matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_electric_cherry mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.electric_cherry matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_tombstone mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.tombstone matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_whos_who mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.whos_who matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_dying_wish mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.dying_wish matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data
scoreboard players set #pool_slot mgs.data 0
execute if score #map_perk_widows_wine mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score #pool_all_perks mgs.data matches 1 run scoreboard players set #pool_slot mgs.data 1
execute if score @n[tag=mgs.pool_target] mgs.zb.perk.widows_wine matches 1 run scoreboard players set #pool_slot mgs.data 0
scoreboard players operation #pool_avail mgs.data += #pool_slot mgs.data

