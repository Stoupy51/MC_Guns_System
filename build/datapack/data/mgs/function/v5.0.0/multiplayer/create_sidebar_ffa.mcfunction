
#> mgs:v5.0.0/multiplayer/create_sidebar_ffa
#
# @within	mgs:v5.0.0/multiplayer/start
#

function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate: "mgs.free_for_all",color:"gold",bold:true},contents:[[{text:" ⏱ ",color:"yellow"},[{score:{name:"#_timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#_timer_tens",objective:"mgs.data"}},{score:{name:"#_timer_ones",objective:"mgs.data"}}]]," ",[{translate: "mgs.first_to",color:"gray"},{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]]}
scoreboard objectives setdisplay sidebar mgs.sidebar

