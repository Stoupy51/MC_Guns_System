
#> mgs:v5.0.0/zombies/pap/repap_scope_only
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap
#
# @args		slot (unknown)
#

# Guard: enough points for scope/camo re-roll
execute unless score @s mgs.zb.points matches 1000.. run return run function mgs:v5.0.0/zombies/pap/deny_not_enough_points_scope

# Deduct points
scoreboard players remove @s mgs.zb.points 1000

# Save current weapon ID and models before scope randomization (for restore)
data modify storage mgs:temp _pap_old_weapon set from storage mgs:temp _pap_extract.weapon
data modify storage mgs:temp _pap_pre_cosm_models set from storage mgs:temp _pap_extract.stats.models
data remove storage mgs:temp _pap_pre_cosm_scope_level
execute if data storage mgs:temp _pap_extract.stats.scope_level run data modify storage mgs:temp _pap_pre_cosm_scope_level set from storage mgs:temp _pap_extract.stats.scope_level

# Randomize weapon scope (retry until different from current)
function mgs:v5.0.0/zombies/pap/randomize_scope_different with storage mgs:temp _pap_extract.stats

# Randomize camo (uses new scope weapon_id, same base_weapon)
function mgs:v5.0.0/zombies/pap/randomize_camo with storage mgs:temp _pap_extract.stats

# Store pending cosmetics (scope + camo) for mid-animation application, keyed by machine ID
data modify storage mgs:temp _pap_cosm_store set value {}
execute store result storage mgs:temp _pap_cosm_store.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
data modify storage mgs:temp _pap_cosm_store.models set from storage mgs:temp _pap_extract.stats.models
data modify storage mgs:temp _pap_cosm_store.weapon set from storage mgs:temp _pap_extract.weapon
execute if data storage mgs:temp _pap_extract.stats.scope_level run data modify storage mgs:temp _pap_cosm_store.scope_level set from storage mgs:temp _pap_extract.stats.scope_level
function mgs:v5.0.0/zombies/pap/anim/store_cosmetics with storage mgs:temp _pap_cosm_store

# Restore original appearance so the item enters the machine with its current look
data modify storage mgs:temp _pap_extract.stats.models set from storage mgs:temp _pap_pre_cosm_models
data modify storage mgs:temp _pap_extract.weapon set from storage mgs:temp _pap_old_weapon
data remove storage mgs:temp _pap_extract.stats.scope_level
execute if data storage mgs:temp _pap_pre_cosm_scope_level run data modify storage mgs:temp _pap_extract.stats.scope_level set from storage mgs:temp _pap_pre_cosm_scope_level

# Apply stats to item (with restored original cosmetics)
$item modify entity @s $(slot) mgs:v5.0.0/zb_pap_apply_stats

# Brief feedback
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.scope_re_rolled_1000_points","color":"aqua"}]

# Start PAP animation
tag @s add mgs.pap_owner
scoreboard players operation @s mgs.zb.pap_s = #pap_sel mgs.data
execute store result score @s mgs.zb.pap_mid run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
execute as @n[tag=bs.interaction.target] at @s run function mgs:v5.0.0/zombies/pap/anim/start with storage mgs:temp _pap
tag @s remove mgs.pap_owner

