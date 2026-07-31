
#> mgs:v5.1.0/multiplayer/build_sidebar_demo
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/refresh_sidebar_demo with storage mgs:temp demo_sb
#
# @args		atk (unknown)
#			a (unknown)
#			b (unknown)
#

scoreboard players reset * mgs.sidebar
$function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate:"mgs.demolition",color:"gold",bold:true},contents:[[" ⏱ ",[{score:{name:"#timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#timer_tens",objective:"mgs.data"}},{score:{name:"#timer_ones",objective:"mgs.data"}}]]," ",[["", " 🔴 ",{translate:"mgs.red",color:"red"}],[" ",{score:{name:"#red",objective:"mgs.mp.team"},color:"white"}]],[["", " 🔵 ",{translate:"mgs.blue",color:"blue"}],[" ",{score:{name:"#blue",objective:"mgs.mp.team"},color:"white"}]]," ",[[{text:" ",color:"gray"}, {translate:"mgs.round"}],{score:{name:"#demo_round",objective:"mgs.data"},color:"white"}],$(atk)," ",$(a),$(b)]}
scoreboard objectives setdisplay sidebar mgs.sidebar

