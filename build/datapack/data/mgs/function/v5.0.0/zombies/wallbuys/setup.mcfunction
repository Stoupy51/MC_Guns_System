
#> mgs:v5.0.0/zombies/wallbuys/setup
#
# @within	mgs:v5.0.0/zombies/preload_complete
#

scoreboard players set #_wb_counter mgs.data 0
data modify storage mgs:zombies wallbuy_data set value {}
data modify storage mgs:temp _wb_iter set from storage mgs:zombies game.map.wallbuys
execute if data storage mgs:temp _wb_iter[0] run function mgs:v5.0.0/zombies/wallbuys/setup_iter

