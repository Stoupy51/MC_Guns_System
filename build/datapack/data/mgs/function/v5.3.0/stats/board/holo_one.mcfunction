
#> mgs:v5.3.0/stats/board/holo_one
#
# @executed	at @s
#
# @within	mgs:v5.3.0/stats/board/holo_tick [ at @s ]
#

execute if entity @s[tag=mgs.lb_shown] unless entity @a[distance=..24] run function mgs:v5.3.0/stats/board/holo_hide
execute if entity @s[tag=!mgs.lb_shown] if entity @a[distance=..24] run function mgs:v5.3.0/stats/board/holo_show

