
#> mgs:v5.1.0/multiplayer/editor/hub_row_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/hub with storage mgs:temp editor
#
# @args		secondary_name (unknown)
#			secondary_scope_name (unknown)
#			secondary_camo_name (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:["",{text:"\ud83d\udd2b "},{translate:"mgs.secondary_2",color:"white"},{text:"$(secondary_name)",color:"green"}],tooltip:{text:"$(secondary_scope_name), $(secondary_camo_name)\nClick to change",color:"gray"},action:{type:"run_command",command:"/trigger mgs.player.config set 106"}}

