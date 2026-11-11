
#> mgs:v5.4.2/multiplayer/build_sidebar_ffa
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/refresh_sidebar_ffa with storage mgs:temp
#
# @args		ffa_sb (unknown)
#

tag @a remove mgs.ffa_candidate
scoreboard players reset * mgs.sidebar
$function #bs.sidebar:create {objective:"mgs.sidebar",display_name:{translate:"mgs.free_for_all",fallback:"Free For All",color:"gold",bold:true},contents:$(ffa_sb)}
scoreboard objectives setdisplay sidebar.team.red mgs.sidebar
scoreboard objectives setdisplay sidebar.team.blue mgs.sidebar
scoreboard objectives setdisplay sidebar.team.gold mgs.sidebar

