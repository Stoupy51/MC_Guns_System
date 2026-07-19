
#> mgs:v5.1.0/multiplayer/create_sidebar_hp
#
# @within	mgs:v5.1.0/multiplayer/start
#

scoreboard players reset * mgs.sidebar
function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate:"mgs.hardpoint",color:"gold",bold:true},contents:[[" ⏱ ",[{score:{name:"#timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#timer_tens",objective:"mgs.data"}},{score:{name:"#timer_ones",objective:"mgs.data"}}]]," ",[["", " 🔴 ",{translate:"mgs.red",color:"red"}],[" ",{score:{name:"#red",objective:"mgs.mp.team"},color:"white"}]],[["", " 🔵 ",{translate:"mgs.blue",color:"blue"}],[" ",{score:{name:"#blue",objective:"mgs.mp.team"},color:"white"}]]," ",[[{text:" ",color:"dark_purple"}, {translate:"mgs.zone"}],{score:{name:"#hp_rotate_sec",objective:"mgs.data"},color:"white"},{translate:"mgs.s_left",color:"gray"}]," ",[[{text:" ",color:"gray"}, {translate:"mgs.first_to"}],{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}
scoreboard objectives setdisplay sidebar mgs.sidebar

