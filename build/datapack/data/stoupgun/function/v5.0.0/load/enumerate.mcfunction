
#> stoupgun:v5.0.0/load/enumerate
#
# @within	#stoupgun:enumerate
#

# If current major is too low, set it to the current major
execute unless score #stoupgun.major load.status matches 5.. run scoreboard players set #stoupgun.major load.status 5

# If current minor is too low, set it to the current minor (only if major is correct)
execute if score #stoupgun.major load.status matches 5 unless score #stoupgun.minor load.status matches 0.. run scoreboard players set #stoupgun.minor load.status 0

# If current patch is too low, set it to the current patch (only if major and minor are correct)
execute if score #stoupgun.major load.status matches 5 if score #stoupgun.minor load.status matches 0 unless score #stoupgun.patch load.status matches 0.. run scoreboard players set #stoupgun.patch load.status 0

