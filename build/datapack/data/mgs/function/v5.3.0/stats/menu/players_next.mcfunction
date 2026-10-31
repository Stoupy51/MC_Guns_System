
#> mgs:v5.3.0/stats/menu/players_next
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/menu/players_list
#			mgs:v5.3.0/stats/menu/players_next
#

execute if score #st_i mgs.data >= #st_end mgs.data run return 0
execute if score #st_i mgs.data >= #st_total mgs.data run return 0

execute store result storage mgs:temp _sp.i int 1 run scoreboard players get #st_i mgs.data
scoreboard players operation #st_t mgs.data = #st_i mgs.data
scoreboard players operation #st_t mgs.data *= #4 mgs.data
execute store result storage mgs:temp _sp.trigger int 1 run scoreboard players add #st_t mgs.data 100000
function mgs:v5.3.0/stats/menu/players_uuid with storage mgs:temp _sp

scoreboard players add #st_i mgs.data 1
function mgs:v5.3.0/stats/menu/players_next

