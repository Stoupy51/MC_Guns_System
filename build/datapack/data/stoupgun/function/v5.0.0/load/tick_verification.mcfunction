
#> stoupgun:v5.0.0/load/tick_verification
#
# @within	#minecraft:tick
#

execute if score #stoupgun.major load.status matches 5 if score #stoupgun.minor load.status matches 0 if score #stoupgun.patch load.status matches 0 run function stoupgun:v5.0.0/tick

