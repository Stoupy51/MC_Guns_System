
#> mgs:v5.4.2/load/enumerate
#
# @within	#mgs:enumerate
#			mgs:v5.4.2/dialog/close_then
#

# If current major is too low, set it to the current major
execute unless score #mgs.major load.status matches 5.. run scoreboard players set #mgs.major load.status 5

# If current minor is too low, set it to the current minor (only if major is correct)
execute if score #mgs.major load.status matches 5 unless score #mgs.minor load.status matches 4.. run scoreboard players set #mgs.minor load.status 4

# If current patch is too low, set it to the current patch (only if major and minor are correct)
execute if score #mgs.major load.status matches 5 if score #mgs.minor load.status matches 4 unless score #mgs.patch load.status matches 2.. run scoreboard players set #mgs.patch load.status 2

