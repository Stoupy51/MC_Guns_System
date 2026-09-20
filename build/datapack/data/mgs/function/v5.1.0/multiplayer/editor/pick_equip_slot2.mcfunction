
#> mgs:v5.1.0/multiplayer/editor/pick_equip_slot2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Snapshot, apply (None clears the slot), commit
data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
execute if score @s mgs.player.config matches 470 run data modify storage mgs:temp editor merge value {equip_slot2:"",equip_slot2_name:"None",equip_slot2_camo:""}
execute if score @s mgs.player.config matches 471 run data modify storage mgs:temp editor merge value {equip_slot2:"frag_grenade",equip_slot2_name:"Frag Grenade",equip_slot2_camo:""}
execute if score @s mgs.player.config matches 472 run data modify storage mgs:temp editor merge value {equip_slot2:"semtex",equip_slot2_name:"Semtex",equip_slot2_camo:""}
execute if score @s mgs.player.config matches 473 run data modify storage mgs:temp editor merge value {equip_slot2:"flash_grenade",equip_slot2_name:"Flash",equip_slot2_camo:""}
execute if score @s mgs.player.config matches 474 run data modify storage mgs:temp editor merge value {equip_slot2:"smoke_grenade",equip_slot2_name:"Smoke",equip_slot2_camo:""}

execute store success score #ed_ok mgs.data run function mgs:v5.1.0/multiplayer/editor/commit_check
execute if score #ed_ok mgs.data matches 0 run return run function mgs:v5.1.0/multiplayer/editor/hub

# None → hub, otherwise pick a camo for the grenade (free)
execute if data storage mgs:temp editor{equip_slot2:""} run return run function mgs:v5.1.0/multiplayer/editor/hub
function mgs:v5.1.0/multiplayer/editor/show_equip2_camo_dialog

