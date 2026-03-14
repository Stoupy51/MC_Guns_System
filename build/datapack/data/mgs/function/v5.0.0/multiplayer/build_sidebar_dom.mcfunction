
#> mgs:v5.0.0/multiplayer/build_sidebar_dom
#
# @within	mgs:v5.0.0/multiplayer/refresh_sidebar_dom with storage mgs:temp dom_sb
#
# @args		a (unknown)
#			b (unknown)
#			c (unknown)
#

$function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate:"mgs.domination",color:"gold",bold:true},contents:[[{text:" ⏱ ",color:"yellow"},[{score:{name:"#timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#timer_tens",objective:"mgs.data"}},{score:{name:"#timer_ones",objective:"mgs.data"}}]]," ",[[{text:" 🔴 ",color:"red"},{translate:"mgs.red"}],[" ",{score:{name:"#red",objective:"mgs.mp.team"},color:"white"}]],[[{text:" 🔵 ",color:"blue"},{translate:"mgs.blue"}],[" ",{score:{name:"#blue",objective:"mgs.mp.team"},color:"white"}]]," ",$(a),$(b),$(c)," ",[[{text:" ",color:"gray"}, {translate:"mgs.first_to"}],{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}

