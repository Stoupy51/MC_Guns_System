
#> mgs:v5.3.0/stats/board/zb_map_trigger
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/dispatch
#

scoreboard players set #lb_step mgs.data 8
scoreboard players operation #lb_t mgs.data = @s mgs.player.config
scoreboard players remove #lb_t mgs.data 3000
scoreboard players operation #lb_f mgs.data = #lb_t mgs.data
scoreboard players operation #lb_f mgs.data %= #lb_step mgs.data
scoreboard players operation #lb_t mgs.data /= #lb_step mgs.data
data modify storage mgs:temp _lb_view set value {kind:"zb_map",filters:1b}
execute store result storage mgs:temp _lb_view.i int 1 run scoreboard players get #lb_t mgs.data
execute store result storage mgs:temp _lb_view.f int 1 run scoreboard players get #lb_f mgs.data
execute store result storage mgs:temp _lb_view.trigger int 1 run scoreboard players operation #lb_t mgs.data *= #lb_step mgs.data
execute store result storage mgs:temp _lb_view.trigger int 1 run scoreboard players add #lb_t mgs.data 3000
function mgs:v5.3.0/stats/board/zb_map_view with storage mgs:temp _lb_view

