
#> mgs:v5.4.0/multiplayer/editor/hub_row_secondary_mags
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/hub with storage mgs:temp editor
#
# @args		secondary_mag_count (unknown)
#

$data modify storage mgs:temp dialog.actions append value {label:["",{text:"\ud83d\udce6 "},{translate:"mgs.secondary_mags",fallback:"Secondary Mags: ",color:"white"},{text:"$(secondary_mag_count)x",color:"green"}],tooltip:[{text:"1 ",color:"gray"}, {translate:"mgs.pt_per_magazine",fallback:"pt per magazine"}],action:{type:"run_command",command:"/trigger mgs.player.config set 107"}}

