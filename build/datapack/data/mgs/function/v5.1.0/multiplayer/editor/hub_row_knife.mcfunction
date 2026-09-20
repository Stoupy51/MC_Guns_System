
#> mgs:v5.1.0/multiplayer/editor/hub_row_knife
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/hub with storage mgs:temp editor
#
# @args		knife_camo_name (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:["",{text:"\ud83d\udd2a "},{translate:"mgs.knife_2",color:"white"},{text:"$(knife_camo_name)",color:"green"}],tooltip:{translate:"mgs.free_cosmetic_onlyclick_to_change",color:"gray"},action:{type:"run_command",command:"/trigger mgs.player.config set 113"}}

