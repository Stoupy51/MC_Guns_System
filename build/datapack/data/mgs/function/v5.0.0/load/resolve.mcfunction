
#> mgs:v5.0.0/load/resolve
#
# @within	#mgs:resolve
#

# If correct version, load the datapack
execute if score #mgs.major load.status matches 5 if score #mgs.minor load.status matches 0 if score #mgs.patch load.status matches 0 run function mgs:v5.0.0/load/main

