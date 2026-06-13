
#> mgs:v5.0.1/multiplayer/editor/hub_row_equip2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/hub with storage mgs:temp editor
#
# @args		equip_slot2_name (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:[{text:"\ud83d\udca3 ",color:"red"},[{translate:"mgs.grenade",color:"white"}, " 2: "],{text:"$(equip_slot2_name)",color:"green"}],tooltip:[{text:"1 ",color:"gray"}, {translate:"mgs.ptclick_to_change"}],action:{type:"run_command",command:"/trigger mgs.player.config set 109"}}

