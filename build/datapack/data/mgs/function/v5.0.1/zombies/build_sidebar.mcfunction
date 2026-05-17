
#> mgs:v5.0.1/zombies/build_sidebar
#
# @within	mgs:v5.0.1/zombies/refresh_sidebar with storage mgs:temp
#
# @args		zb_sb (unknown)
#

scoreboard players reset * mgs.zb_sidebar
$function #bs.sidebar:create {objective:"mgs.zb_sidebar",display_name:{translate:"mgs.zombies",color:"dark_green",bold:true},contents:$(zb_sb)}

