
#> mgs:v5.4.2/stats/board/filters
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/stats/board/show with storage mgs:temp _lb_view
#
# @args		trigger (unknown)
#

$scoreboard players set #lb_t mgs.data $(trigger)
execute store result storage mgs:temp _lb_view.f0 int 1 run scoreboard players add #lb_t mgs.data 0
execute store result storage mgs:temp _lb_view.f1 int 1 run scoreboard players add #lb_t mgs.data 1
execute store result storage mgs:temp _lb_view.f2 int 1 run scoreboard players add #lb_t mgs.data 1
execute store result storage mgs:temp _lb_view.f3 int 1 run scoreboard players add #lb_t mgs.data 1
execute store result storage mgs:temp _lb_view.f4 int 1 run scoreboard players add #lb_t mgs.data 1
function mgs:v5.4.2/stats/board/filters_add with storage mgs:temp _lb_view

