
#> mgs:v5.1.0/zombies/inventory/place_perk_item
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"juggernog",name:"Juggernog",color:"red"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"speed_cola",name:"Speed Cola",color:"green"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"double_tap",name:"Double Tap",color:"yellow"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"quick_revive",name:"Quick Revive",color:"aqua"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"mule_kick",name:"Mule Kick",color:"dark_green"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"stamin_up",name:"Stamin-Up",color:"gold"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"phd_flopper",name:"PhD Flopper",color:"dark_purple"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"deadshot",name:"Deadshot Daiquiri",color:"dark_green"}
#			mgs:v5.1.0/zombies/inventory/refresh_perk_items {id:"timeslip",name:"Timeslip",color:"light_purple"}
#
# @args		id (string)
#			name (string)
#			color (string)
#

$data modify storage mgs:temp _perk_place set value {id:"$(id)",name:"$(name)",color:"$(color)"}
execute store result storage mgs:temp _perk_place.slot int 1 run scoreboard players get #perk_inv_slot mgs.data
function mgs:v5.1.0/zombies/inventory/place_perk_item_at with storage mgs:temp _perk_place
scoreboard players remove #perk_inv_slot mgs.data 1

