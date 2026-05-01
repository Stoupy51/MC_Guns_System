
#> mgs:v5.0.0/zombies/pap/free_scope_reroll
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.0.0/zombies/pap/on_free_pap with storage mgs:temp _pap
#

# Randomize scope (guaranteed different from current)
function mgs:v5.0.0/zombies/pap/randomize_scope_different with storage mgs:temp _pap_extract.stats

# Randomize camo on top of the new scope
function mgs:v5.0.0/zombies/pap/randomize_camo with storage mgs:temp _pap_extract.stats

# Set up name data with current (max) level
data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.current_name
execute store result storage mgs:temp _pap_name_data.level int 1 run scoreboard players get #pap_level mgs.data
execute store result storage mgs:temp _pap_name_data.max int 1 run scoreboard players get #pap_max mgs.data

# Apply new cosmetics directly
function mgs:v5.0.0/zombies/pap/apply_to_slot with storage mgs:temp _pap

# Notify the player
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.free_scope_camo_reroll_already_at_max_pap_level","color":"aqua"}]
function mgs:v5.0.0/zombies/feedback/sound_success

