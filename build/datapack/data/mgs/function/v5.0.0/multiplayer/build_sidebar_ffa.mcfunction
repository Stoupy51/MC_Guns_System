
#> mgs:v5.0.0/multiplayer/build_sidebar_ffa
#
# @within	mgs:v5.0.0/multiplayer/refresh_sidebar_ffa with storage mgs:temp
#
# @args		ffa_sb (unknown)
#

tag @a remove mgs.ffa_candidate
scoreboard objectives remove mgs.sidebar
$function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate:"mgs.free_for_all",color:"gold",bold:true},contents:$(ffa_sb)}
scoreboard objectives setdisplay sidebar mgs.sidebar

