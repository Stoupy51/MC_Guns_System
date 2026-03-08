
#> mgs:v5.0.0/multiplayer/create_sidebar_hp
#
# @within	mgs:v5.0.0/multiplayer/start
#

function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate: "mgs.hardpoint",color:"gold",bold:true},contents:[[{text:" ⏱ ",color:"yellow"},[{score:{name:"#timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#timer_tens",objective:"mgs.data"}},{score:{name:"#timer_ones",objective:"mgs.data"}}]]," ",[[{text:" 🔴 ",color:"red"},{translate: "mgs.red"}],[" ",{score:{name:"#red",objective:"mgs.mp.team"},color:"white"}]],[[{text:" 🔵 ",color:"blue"},{translate: "mgs.blue"}],[" ",{score:{name:"#blue",objective:"mgs.mp.team"},color:"white"}]]," ",[{translate: "mgs.zone",color:"dark_purple"},{score:{name:"#hp_rotate_sec",objective:"mgs.data"},color:"white"},{translate: "mgs.s_left",color:"gray"}]," ",[{translate: "mgs.first_to",color:"gray"},{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}
scoreboard objectives setdisplay sidebar mgs.sidebar

