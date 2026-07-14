
#> mgs:v5.1.0/multiplayer/editor/hub_row_perks
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/multiplayer/editor/hub with storage mgs:temp _hub
#
# @args		perks (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:[{text:"\u2b50 ",color:"aqua"},{translate:"mgs.perks_2",color:"white"},{text:"$(perks)/3",color:"green"}],tooltip:[{text:"1 ",color:"gray"}, {translate:"mgs.pt_per_perk"}],action:{type:"run_command",command:"/trigger mgs.player.config set 110"}}

