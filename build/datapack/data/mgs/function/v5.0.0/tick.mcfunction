
#> mgs:v5.0.0/tick
#
# @within	mgs:v5.0.0/load/tick_verification
#

# Player loop
execute as @a[sort=random] at @s run function mgs:v5.0.0/player/tick

# Tick function for flashes
execute if score #flash_count mgs.data matches 1.. as @e[tag=mgs.flash] run function mgs:v5.0.0/flash/tick

