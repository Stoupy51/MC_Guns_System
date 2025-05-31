
#> mgs:v5.0.0/load/main
#
# @within	mgs:v5.0.0/load/resolve
#

# Avoiding multiple executions of the same load function
execute unless score #mgs.loaded load.status matches 1 run function mgs:v5.0.0/load/secondary

