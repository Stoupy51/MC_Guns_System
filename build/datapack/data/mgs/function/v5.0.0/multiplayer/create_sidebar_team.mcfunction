
#> mgs:v5.0.0/multiplayer/create_sidebar_team
#
# @within	mgs:v5.0.0/multiplayer/start {title:"Team Deathmatch"}
#			mgs:v5.0.0/multiplayer/start {title:"Search & Destroy"}
#
# @args		title (string)
#

scoreboard objectives remove mgs.sidebar
$function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{text:"$(title)",color:"gold",bold:true},contents:[[{text:" ⏱ ",color:"yellow"},[{score:{name:"#timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#timer_tens",objective:"mgs.data"}},{score:{name:"#timer_ones",objective:"mgs.data"}}]]," ",[[{text:" 🔴 ",color:"red"},{translate:"mgs.red"}],[" ",{score:{name:"#red",objective:"mgs.mp.team"},color:"white"}]],[[{text:" 🔵 ",color:"blue"},{translate:"mgs.blue"}],[" ",{score:{name:"#blue",objective:"mgs.mp.team"},color:"white"}]]," ",[[{text:" ",color:"gray"}, {translate:"mgs.first_to"}],{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}
scoreboard objectives setdisplay sidebar mgs.sidebar

