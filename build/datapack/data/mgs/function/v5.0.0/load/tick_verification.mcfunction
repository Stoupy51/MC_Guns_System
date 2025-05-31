
#> mgs:v5.0.0/load/tick_verification
#
# @within	#minecraft:tick
#

execute if score #mgs.major load.status matches 5 if score #mgs.minor load.status matches 0 if score #mgs.patch load.status matches 0 run function mgs:v5.0.0/tick

