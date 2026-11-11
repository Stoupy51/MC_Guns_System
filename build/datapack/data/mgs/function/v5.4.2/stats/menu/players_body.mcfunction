
#> mgs:v5.4.2/stats/menu/players_body
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/menu/players_list with storage mgs:temp _sp
#
# @args		total (unknown)
#

$data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:["",{translate:"mgs.known_players",fallback:"Known players",color:"gray"},": ",{text:"$(total)",color:"white"}]}

