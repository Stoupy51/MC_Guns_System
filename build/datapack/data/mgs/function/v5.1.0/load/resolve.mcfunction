
#> mgs:v5.1.0/load/resolve
#
# @within	#mgs:resolve
#

# If correct version, load the datapack
execute if score #mgs.major load.status matches 5 if score #mgs.minor load.status matches 1 if score #mgs.patch load.status matches 0 run function mgs:v5.1.0/load/main

