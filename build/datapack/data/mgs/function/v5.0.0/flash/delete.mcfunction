
#> mgs:v5.0.0/flash/delete
#
# @within	mgs:v5.0.0/flash/tick
#

# Decrease flash entity counter and kill entity
scoreboard players remove #flash_count mgs.data 1
kill @s

