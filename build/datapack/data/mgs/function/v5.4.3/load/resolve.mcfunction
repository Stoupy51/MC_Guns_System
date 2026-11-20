
#> mgs:v5.4.3/load/resolve
#
# @within	#mgs:resolve
#			mgs:v5.4.3/dialog/close_then
#

# If correct version, load the datapack
execute if score #mgs.major load.status matches 5 if score #mgs.minor load.status matches 4 if score #mgs.patch load.status matches 3 run function mgs:v5.4.3/load/main

