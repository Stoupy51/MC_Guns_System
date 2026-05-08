
#> mgs:v5.0.1/zombies/create_sidebar
#
# @within	mgs:v5.0.1/zombies/preload_complete
#

scoreboard objectives add mgs.zb_sidebar dummy
function mgs:v5.0.1/zombies/refresh_sidebar
scoreboard objectives setdisplay sidebar mgs.zb_sidebar

