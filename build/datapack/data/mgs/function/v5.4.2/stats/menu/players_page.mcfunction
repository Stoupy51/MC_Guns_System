
#> mgs:v5.4.2/stats/menu/players_page
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/config/process
#

scoreboard players operation #st_page mgs.data = @s mgs.player.config
scoreboard players remove #st_page mgs.data 90000
function mgs:v5.4.2/stats/menu/players_list {kind:"view",title:"Players"}

