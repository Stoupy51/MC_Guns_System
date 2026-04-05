
#> mgs:v5.0.0/zombies/pap/annotate_pellets_line
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/annotate_lore
#

execute store result score #pap_old mgs.data run data get storage mgs:temp _pap_old_stats.pellet_count
execute store result score #pap_new mgs.data run data get storage mgs:temp _pap_extract.stats.pellet_count
scoreboard players operation #pap_delta mgs.data = #pap_new mgs.data
scoreboard players operation #pap_delta mgs.data -= #pap_old mgs.data
execute unless score #pap_delta mgs.data matches 0 run function mgs:v5.0.0/zombies/pap/annotate_int_delta
scoreboard players add #pap_li mgs.data 1

