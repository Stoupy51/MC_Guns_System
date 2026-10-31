
#> mgs:v5.3.0/stats/menu/mine
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/config/process
#

scoreboard players operation #st_i mgs.data = @s mgs.st.index
scoreboard players set #st_m mgs.data 0
function mgs:v5.3.0/stats/menu/view

