
#> mgs:v5.0.0/weapon/dps_collect
#
# @within	#mgs:signals/on_hit_entity
#

# @s = hit entity; add damage (x10) to the shooter's DPS accumulator
execute store result score #sent_damage mgs.data run data get storage mgs:signals on_hit_entity.damage 10
scoreboard players operation @a[tag=mgs.ticking,limit=1] mgs.dps += #sent_damage mgs.data

