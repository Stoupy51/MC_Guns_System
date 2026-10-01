
#> mgs:v5.1.0/zombies/pap/free_scope_reroll
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.1.0/zombies/pap/upgrade_core with storage mgs:temp _pap
#

function mgs:v5.1.0/zombies/pap/randomize_scope_different with storage mgs:temp _pap_extract.stats

function mgs:v5.1.0/zombies/pap/randomize_camo with storage mgs:temp _pap_extract.stats

data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.current_name
execute store result storage mgs:temp _pap_name_data.level int 1 run scoreboard players get #pap_level mgs.data
execute store result storage mgs:temp _pap_name_data.max int 1 run scoreboard players get #pap_max mgs.data

function mgs:v5.1.0/zombies/pap/apply_to_slot with storage mgs:temp _pap

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"✦ ",{"translate":"mgs.free_scope_camo_reroll_already_at_max_pap_level","color":"aqua"}]
playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25

