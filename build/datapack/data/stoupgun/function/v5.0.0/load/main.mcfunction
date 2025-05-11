
#> stoupgun:v5.0.0/load/main
#
# @within	stoupgun:v5.0.0/load/resolve
#

# Avoiding multiple executions of the same load function
execute unless score #stoupgun.loaded load.status matches 1 run function stoupgun:v5.0.0/load/secondary

