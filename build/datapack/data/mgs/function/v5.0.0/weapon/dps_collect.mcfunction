
#> mgs:v5.0.0/weapon/dps_collect
#
# @within	#mgs:signals/damage
#
# @args		amount (unknown)
#

# @s = hit entity; add damage (x10) to the shooter's DPS accumulator
# Store $(amount) float then read back x10 to get integer tenths (same unit as dps accumulator)
$data modify storage mgs:temp dps_amount set value $(amount)
execute store result score #sent_damage mgs.data run data get storage mgs:temp dps_amount 10
scoreboard players operation @n[tag=mgs.ticking] mgs.dps += #sent_damage mgs.data

