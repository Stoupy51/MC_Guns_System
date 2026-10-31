
#> mgs:v5.3.0/stats/board/maps_next
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/maps
#			mgs:v5.3.0/stats/board/maps_next
#

execute unless data storage mgs:temp _lb_maps[0] run return 0
execute store result storage mgs:temp _lb_maps[0].trigger int 1 run scoreboard players get #lb_t mgs.data
function mgs:v5.3.0/stats/board/maps_button with storage mgs:temp _lb_maps[0]
scoreboard players operation #lb_t mgs.data += #lb_step mgs.data
data remove storage mgs:temp _lb_maps[0]
function mgs:v5.3.0/stats/board/maps_next

