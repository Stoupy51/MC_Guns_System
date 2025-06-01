
#> mgs:v5.0.0/flash/tick
#
# @within	mgs:v5.0.0/tick
#

# Decrement life time
scoreboard players remove @s mgs.data 1

# Kill flash after 1 tick (50 ms)
execute if score @s mgs.data matches -2 run function mgs:v5.0.0/flash/delete

