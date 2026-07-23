
#> mgs:v5.1.0/zombies/inventory/refresh_perk_items
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	#mgs:zombies/on_new_perk
#			mgs:v5.1.0/zombies/inventory/refresh_info_item
#			mgs:v5.1.0/zombies/perks/tombstone_collect
#			mgs:v5.1.0/zombies/perks/lose_all
#			mgs:v5.1.0/zombies/whos_who/revive_complete
#

# Wipe previous perk display items (owned set may have shrunk), then re-place from slot 26 down
execute if items entity @s inventory.26 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.26 with air
execute if items entity @s inventory.25 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.25 with air
execute if items entity @s inventory.24 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.24 with air
execute if items entity @s inventory.23 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.23 with air
execute if items entity @s inventory.22 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.22 with air
execute if items entity @s inventory.21 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.21 with air
execute if items entity @s inventory.20 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.20 with air
execute if items entity @s inventory.19 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.19 with air
execute if items entity @s inventory.18 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.18 with air
execute if items entity @s inventory.17 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.17 with air
execute if items entity @s inventory.16 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.16 with air
execute if items entity @s inventory.15 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.15 with air
execute if items entity @s inventory.14 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.14 with air
execute if items entity @s inventory.13 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.13 with air
scoreboard players set #perk_inv_slot mgs.data 26
execute if score @s mgs.zb.perk.juggernog matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/juggernog
execute if score @s mgs.zb.perk.speed_cola matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/speed_cola
execute if score @s mgs.zb.perk.double_tap matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/double_tap
execute if score @s mgs.zb.perk.quick_revive matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/quick_revive
execute if score @s mgs.zb.perk.mule_kick matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/mule_kick
execute if score @s mgs.zb.perk.stamin_up matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/stamin_up
execute if score @s mgs.zb.perk.phd_flopper matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/phd_flopper
execute if score @s mgs.zb.perk.deadshot matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/deadshot
execute if score @s mgs.zb.perk.timeslip matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/timeslip
execute if score @s mgs.zb.perk.electric_cherry matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/electric_cherry
execute if score @s mgs.zb.perk.tombstone matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/tombstone
execute if score @s mgs.zb.perk.whos_who matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/whos_who
execute if score @s mgs.zb.perk.dying_wish matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/dying_wish
execute if score @s mgs.zb.perk.widows_wine matches 1 run function mgs:v5.1.0/zombies/inventory/place_perk/widows_wine

