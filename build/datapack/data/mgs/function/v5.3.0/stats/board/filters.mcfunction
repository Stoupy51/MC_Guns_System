
#> mgs:v5.3.0/stats/board/filters
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/show with storage mgs:temp _lb_view
#
# @args		trigger (unknown)
#

$scoreboard players set #lb_t mgs.data $(trigger)
execute store result storage mgs:temp _lb_view.f0 int 1 run scoreboard players add #lb_t mgs.data 0
execute store result storage mgs:temp _lb_view.f1 int 1 run scoreboard players add #lb_t mgs.data 1
execute store result storage mgs:temp _lb_view.f2 int 1 run scoreboard players add #lb_t mgs.data 1
execute store result storage mgs:temp _lb_view.f3 int 1 run scoreboard players add #lb_t mgs.data 1
execute store result storage mgs:temp _lb_view.f4 int 1 run scoreboard players add #lb_t mgs.data 1
function mgs:v5.3.0/stats/board/filters_add with storage mgs:temp _lb_view

