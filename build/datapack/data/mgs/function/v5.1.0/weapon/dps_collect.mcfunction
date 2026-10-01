
#> mgs:v5.1.0/weapon/dps_collect
#
# @within	#mgs:signals/damage
#
# @args		amount (unknown)
#

# Stored as a float, read back x10 into integer tenths, the accumulator's unit.
$data modify storage mgs:temp dps_amount set value $(amount)
execute store result score #sent_damage mgs.data run data get storage mgs:temp dps_amount 10
scoreboard players operation @n[tag=mgs.ticking] mgs.dps += #sent_damage mgs.data

