
#> mgs:v5.0.0/zombies/pap/annotate_fire_rate_line
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/annotate_lore
#

execute store result score #pap_old mgs.data run data get storage mgs:temp _pap_old_stats.cooldown
execute store result score #pap_new mgs.data run data get storage mgs:temp _pap_extract.stats.cooldown

# Compute fire rate in tenths: 200 / cooldown
scoreboard players operation #pap_rate_old mgs.data = #200 mgs.data
scoreboard players operation #pap_rate_old mgs.data /= #pap_old mgs.data
scoreboard players operation #pap_rate_new mgs.data = #200 mgs.data
scoreboard players operation #pap_rate_new mgs.data /= #pap_new mgs.data

scoreboard players operation #pap_delta mgs.data = #pap_rate_new mgs.data
scoreboard players operation #pap_delta mgs.data -= #pap_rate_old mgs.data

# Annotate if rate changed
execute store result storage mgs:temp _pap_ann.index int 1 run scoreboard players get #pap_li mgs.data
execute unless score #pap_delta mgs.data matches 0 run function mgs:v5.0.0/zombies/pap/annotate_rate_delta
scoreboard players add #pap_li mgs.data 1

