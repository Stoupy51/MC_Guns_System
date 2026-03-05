
#> mgs:v5.0.0/multiplayer/create_sidebar_team
#
# @within	mgs:v5.0.0/multiplayer/start {title:"Team Deathmatch"}
#			mgs:v5.0.0/multiplayer/start {title:"Domination"}
#			mgs:v5.0.0/multiplayer/start {title:"Hardpoint"}
#			mgs:v5.0.0/multiplayer/start {title:"Search & Destroy"}
#
# @args		title (string)
#

$function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{text:"$(title)",color:"gold",bold:true},contents:[[{text:" ⏱ ",color:"yellow"},["",{score:{name:"#_timer_min",objective:"mgs.data"},color:"yellow"},{text:":",color:"yellow"},{score:{name:"#_timer_tens",objective:"mgs.data"},color:"yellow"},{score:{name:"#_timer_ones",objective:"mgs.data"},color:"yellow"}]],{text:" "},[{text:" 🔴 Red ",color:"red"},{score:{name:"#red",objective:"mgs.mp.team"},color:"white"}],[{text:" 🔵 Blue ",color:"blue"},{score:{name:"#blue",objective:"mgs.mp.team"},color:"white"}],{text:" "},[{translate: "mgs.first_to",color:"gray"},{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}
scoreboard objectives setdisplay sidebar mgs.sidebar

