
#> mgs:v5.0.1/zombies/inventory/refresh_perk_items
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	#mgs:zombies/on_new_perk
#			mgs:v5.0.1/zombies/inventory/refresh_info_item
#			mgs:v5.0.1/zombies/perks/lose_all
#

# Wipe previous perk display items (owned set may have shrunk), then re-place from slot 26 down
execute if items entity @s inventory.26 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.26 with air
execute if items entity @s inventory.25 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.25 with air
execute if items entity @s inventory.24 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.24 with air
execute if items entity @s inventory.23 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.23 with air
execute if items entity @s inventory.22 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.22 with air
execute if items entity @s inventory.21 *[custom_data~{mgs:{zb_perk_display:true}}] run item replace entity @s inventory.21 with air
scoreboard players set #perk_inv_slot mgs.data 26
execute if score @s mgs.zb.perk.juggernog matches 1 run function mgs:v5.0.1/zombies/inventory/place_perk_item {id:"juggernog",name:"Juggernog",color:"red"}
execute if score @s mgs.zb.perk.speed_cola matches 1 run function mgs:v5.0.1/zombies/inventory/place_perk_item {id:"speed_cola",name:"Speed Cola",color:"green"}
execute if score @s mgs.zb.perk.double_tap matches 1 run function mgs:v5.0.1/zombies/inventory/place_perk_item {id:"double_tap",name:"Double Tap",color:"yellow"}
execute if score @s mgs.zb.perk.quick_revive matches 1 run function mgs:v5.0.1/zombies/inventory/place_perk_item {id:"quick_revive",name:"Quick Revive",color:"aqua"}
execute if score @s mgs.zb.perk.mule_kick matches 1 run function mgs:v5.0.1/zombies/inventory/place_perk_item {id:"mule_kick",name:"Mule Kick",color:"dark_green"}
execute if score @s mgs.zb.perk.stamin_up matches 1 run function mgs:v5.0.1/zombies/inventory/place_perk_item {id:"stamin_up",name:"Stamin-Up",color:"gold"}

