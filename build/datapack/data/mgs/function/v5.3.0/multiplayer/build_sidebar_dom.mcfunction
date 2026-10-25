
#> mgs:v5.3.0/multiplayer/build_sidebar_dom
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/multiplayer/refresh_sidebar_dom with storage mgs:temp dom_sb
#
# @args		a (unknown)
#			b (unknown)
#			c (unknown)
#

scoreboard players reset * mgs.sidebar
$function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate:"mgs.domination",fallback:"Domination",color:"gold",bold:true},contents:[[" ⏱ ",[{score:{name:"#timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#timer_tens",objective:"mgs.data"}},{score:{name:"#timer_ones",objective:"mgs.data"}}]]," ",[["", " 🔴 ",{translate:"mgs.red",fallback:"Red",color:"red"}],[" ",{score:{name:"#red",objective:"mgs.mp.team"},color:"white"}]],[["", " 🔵 ",{translate:"mgs.blue",fallback:"Blue",color:"blue"}],[" ",{score:{name:"#blue",objective:"mgs.mp.team"},color:"white"}]]," ",$(a),$(b),$(c)," ",[[{text:" ",color:"gray"}, {translate:"mgs.first_to",fallback:"First to "}],{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}
scoreboard objectives setdisplay sidebar.team.red mgs.sidebar
scoreboard objectives setdisplay sidebar.team.blue mgs.sidebar
scoreboard objectives setdisplay sidebar.team.gold mgs.sidebar

