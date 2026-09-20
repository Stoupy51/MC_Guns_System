
#> mgs:v5.1.0/multiplayer/editor/pick_equip_slot1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Snapshot, apply (None clears the slot), commit
data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
execute if score @s mgs.player.config matches 460 run data modify storage mgs:temp editor merge value {equip_slot1:"",equip_slot1_name:"None",equip_slot1_camo:""}
execute if score @s mgs.player.config matches 461 run data modify storage mgs:temp editor merge value {equip_slot1:"frag_grenade",equip_slot1_name:"Frag Grenade",equip_slot1_camo:""}
execute if score @s mgs.player.config matches 462 run data modify storage mgs:temp editor merge value {equip_slot1:"semtex",equip_slot1_name:"Semtex",equip_slot1_camo:""}
execute if score @s mgs.player.config matches 463 run data modify storage mgs:temp editor merge value {equip_slot1:"flash_grenade",equip_slot1_name:"Flash",equip_slot1_camo:""}
execute if score @s mgs.player.config matches 464 run data modify storage mgs:temp editor merge value {equip_slot1:"smoke_grenade",equip_slot1_name:"Smoke",equip_slot1_camo:""}

execute store success score #ed_ok mgs.data run function mgs:v5.1.0/multiplayer/editor/commit_check
execute if score #ed_ok mgs.data matches 0 run return run function mgs:v5.1.0/multiplayer/editor/hub

# None → hub, otherwise pick a camo for the grenade (free)
execute if data storage mgs:temp editor{equip_slot1:""} run return run function mgs:v5.1.0/multiplayer/editor/hub
function mgs:v5.1.0/multiplayer/editor/show_equip1_camo_dialog

