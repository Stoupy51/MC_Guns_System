
#> mgs:v5.1.0/multiplayer/editor/hub_row_primary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/hub with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			primary_scope_name (unknown)
#			primary_camo_name (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:[{text:"\ud83d\udd2b ",color:"gold"},{translate:"mgs.primary_2",color:"white"},{text:"$(primary_name)",color:"green"}],tooltip:{text:"$(primary_scope_name), $(primary_camo_name)\nClick to change",color:"gray"},action:{type:"run_command",command:"/trigger mgs.player.config set 104"}}

