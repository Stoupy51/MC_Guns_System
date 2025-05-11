
#> stoupgun:v5.0.0/load/resolve
#
# @within	#stoupgun:resolve
#

# If correct version, load the datapack
execute if score #stoupgun.major load.status matches 5 if score #stoupgun.minor load.status matches 0 if score #stoupgun.patch load.status matches 0 run function stoupgun:v5.0.0/load/main

