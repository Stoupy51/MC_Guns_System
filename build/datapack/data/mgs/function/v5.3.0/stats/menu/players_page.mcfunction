
#> mgs:v5.3.0/stats/menu/players_page
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/config/process
#

scoreboard players operation #st_page mgs.data = @s mgs.player.config
scoreboard players remove #st_page mgs.data 90000
function mgs:v5.3.0/stats/menu/players_list {kind:"view",title:"Players"}

