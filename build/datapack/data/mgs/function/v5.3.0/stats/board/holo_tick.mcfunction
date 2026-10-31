
#> mgs:v5.3.0/stats/board/holo_tick
#
# @within	mgs:v5.3.0/zombies/preload_complete 1s replace [ scheduled ]
#			mgs:v5.3.0/stats/board/holo_tick 1s replace [ scheduled ]
#

execute as @e[type=minecraft:marker,tag=mgs.leaderboard] at @s run function mgs:v5.3.0/stats/board/holo_one
execute if entity @e[type=minecraft:marker,tag=mgs.leaderboard] run schedule function mgs:v5.3.0/stats/board/holo_tick 1s replace

