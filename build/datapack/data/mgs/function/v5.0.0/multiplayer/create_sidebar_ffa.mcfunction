
#> mgs:v5.0.0/multiplayer/create_sidebar_ffa
#
# @within	mgs:v5.0.0/multiplayer/start
#

function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate: "mgs.free_for_all",color:"gold",bold:true},contents:[[{text:" ⏱ ",color:"yellow"},["",{score:{name:"#_timer_min",objective:"mgs.data"},color:"yellow"},{text:":",color:"yellow"},{score:{name:"#_timer_tens",objective:"mgs.data"},color:"yellow"},{score:{name:"#_timer_ones",objective:"mgs.data"},color:"yellow"}]],{text:" "},[{translate: "mgs.first_to",color:"gray"},{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}
scoreboard objectives setdisplay sidebar mgs.sidebar

