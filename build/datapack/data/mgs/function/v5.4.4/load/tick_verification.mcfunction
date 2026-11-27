
#> mgs:v5.4.4/load/tick_verification
#
# @within	#minecraft:tick
#			mgs:v5.4.4/dialog/close_then
#

execute if score #mgs.major load.status matches 5 if score #mgs.minor load.status matches 4 if score #mgs.patch load.status matches 4 run function mgs:v5.4.4/tick

