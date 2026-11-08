
#> mgs:v5.4.1/load/main
#
# @within	mgs:v5.4.1/load/resolve
#			mgs:v5.4.1/dialog/close_then
#

# Avoiding multiple executions of the same load function
execute unless score #mgs.loaded load.status matches 1 run function mgs:v5.4.1/load/secondary

