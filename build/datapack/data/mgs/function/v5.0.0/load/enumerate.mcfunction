
#> mgs:v5.0.0/load/enumerate
#
# @within	#mgs:enumerate
#

# If current major is too low, set it to the current major
execute unless score #mgs.major load.status matches 5.. run scoreboard players set #mgs.major load.status 5

# If current minor is too low, set it to the current minor (only if major is correct)
execute if score #mgs.major load.status matches 5 unless score #mgs.minor load.status matches 0.. run scoreboard players set #mgs.minor load.status 0

# If current patch is too low, set it to the current patch (only if major and minor are correct)
execute if score #mgs.major load.status matches 5 if score #mgs.minor load.status matches 0 unless score #mgs.patch load.status matches 0.. run scoreboard players set #mgs.patch load.status 0

