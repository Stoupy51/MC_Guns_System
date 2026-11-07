
#> mgs:v5.4.0/multiplayer/editor/hub_row_perks
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/hub with storage mgs:temp _hub
#
# @args		perks (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:["",{text:"\u2b50 "},{translate:"mgs.perks_2",fallback:"Perks: ",color:"white"},{text:"$(perks)/3",color:"green"}],tooltip:[{text:"1 ",color:"gray"}, {translate:"mgs.pt_per_perk",fallback:"pt per perk"}],action:{type:"run_command",command:"/trigger mgs.player.config set 110"}}

