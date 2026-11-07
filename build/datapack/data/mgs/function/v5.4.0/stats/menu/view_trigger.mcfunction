
#> mgs:v5.4.0/stats/menu/view_trigger
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/player/config/process
#

scoreboard players operation #st_m mgs.data = @s mgs.player.config
scoreboard players remove #st_m mgs.data 100000
scoreboard players operation #st_i mgs.data = #st_m mgs.data
scoreboard players operation #st_i mgs.data /= #4 mgs.data
scoreboard players operation #st_m mgs.data %= #4 mgs.data
function mgs:v5.4.0/stats/menu/view

