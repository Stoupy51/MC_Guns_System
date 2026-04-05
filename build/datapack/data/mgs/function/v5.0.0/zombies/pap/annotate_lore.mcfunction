
#> mgs:v5.0.0/zombies/pap/annotate_lore
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click
#

scoreboard players set #pap_li mgs.data 0
execute store result score #pap_old mgs.data run data get storage mgs:temp _pap_old_stats.damage
execute store result score #pap_new mgs.data run data get storage mgs:temp _pap_extract.stats.damage
scoreboard players operation #pap_delta mgs.data = #pap_new mgs.data
scoreboard players operation #pap_delta mgs.data -= #pap_old mgs.data
execute unless score #pap_delta mgs.data matches 0 run function mgs:v5.0.0/zombies/pap/annotate_int_delta
scoreboard players add #pap_li mgs.data 1
scoreboard players add #pap_li mgs.data 1
execute store result score #pap_old mgs.data run data get storage mgs:temp _pap_old_stats.reload_time
execute store result score #pap_new mgs.data run data get storage mgs:temp _pap_extract.stats.reload_time
scoreboard players operation #pap_delta mgs.data = #pap_new mgs.data
scoreboard players operation #pap_delta mgs.data -= #pap_old mgs.data
execute unless score #pap_delta mgs.data matches 0 run function mgs:v5.0.0/zombies/pap/annotate_time_delta
scoreboard players add #pap_li mgs.data 1
execute if data storage mgs:temp _pap_extract.stats.cooldown run function mgs:v5.0.0/zombies/pap/annotate_fire_rate_line
execute if data storage mgs:temp _pap_extract.stats.pellet_count run function mgs:v5.0.0/zombies/pap/annotate_pellets_line
execute store result score #pap_old mgs.data run data get storage mgs:temp _pap_old_stats.decay 100
execute store result score #pap_new mgs.data run data get storage mgs:temp _pap_extract.stats.decay 100
scoreboard players operation #pap_delta mgs.data = #pap_new mgs.data
scoreboard players operation #pap_delta mgs.data -= #pap_old mgs.data
execute unless score #pap_delta mgs.data matches 0 run function mgs:v5.0.0/zombies/pap/annotate_pct_delta
scoreboard players add #pap_li mgs.data 1
execute store result score #pap_old mgs.data run data get storage mgs:temp _pap_old_stats.switch
execute store result score #pap_new mgs.data run data get storage mgs:temp _pap_extract.stats.switch
scoreboard players operation #pap_delta mgs.data = #pap_new mgs.data
scoreboard players operation #pap_delta mgs.data -= #pap_old mgs.data
execute unless score #pap_delta mgs.data matches 0 run function mgs:v5.0.0/zombies/pap/annotate_time_delta

