
#> mgs:v5.3.0/stats/menu/players_body
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_list with storage mgs:temp _sp
#
# @args		total (unknown)
#

$data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:["",{translate:"mgs.known_players",fallback:"Known players",color:"gray"},": ",{text:"$(total)",color:"white"}]}

