
#> mgs:v5.0.0/zombies/pap/repap_scope_only
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap
#
# @args		slot (unknown)
#

# Guard: weapon must have at least 2 scope variants to re-roll
data remove storage mgs:temp _pap_scope_check
data modify storage mgs:temp _pap_scope_bw.base_weapon set from storage mgs:temp _pap_extract.stats.base_weapon
function mgs:v5.0.0/zombies/pap/check_scope_variants with storage mgs:temp _pap_scope_bw
execute unless score #pap_has_scopes mgs.data matches 1 run return run function mgs:v5.0.0/zombies/pap/deny_no_scope_variants

# Guard: enough points for scope re-roll
execute unless score @s mgs.zb.points matches 1000.. run return run function mgs:v5.0.0/zombies/pap/deny_not_enough_points_scope

# Deduct points
scoreboard players remove @s mgs.zb.points 1000

# Save current weapon ID to ensure we get a different scope
data modify storage mgs:temp _pap_old_weapon set from storage mgs:temp _pap_extract.weapon

# Randomize weapon scope (retry until different from current)
function mgs:v5.0.0/zombies/pap/randomize_scope_different

# Randomize camo (uses new scope weapon_id, same base_weapon)
function mgs:v5.0.0/zombies/pap/randomize_camo with storage mgs:temp _pap_extract.stats

# Apply updated stats + weapon ID to the item (zb_pap_apply_stats replaces both)
$item modify entity @s $(slot) mgs:v5.0.0/zb_pap_apply_stats

# Update item model to match the new scope + camo
$data modify storage mgs:temp _pap_scope_model.slot set value "$(slot)"
data modify storage mgs:temp _pap_scope_model.model set from storage mgs:temp _pap_extract.stats.models.normal
function mgs:v5.0.0/zombies/pap/set_item_model_from_scope with storage mgs:temp _pap_scope_model

# Brief feedback
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.scope_re_rolled_1000_points","color":"aqua"}]

# Start PAP animation
tag @s add mgs.pap_owner
scoreboard players operation @s mgs.zb.pap_s = #pap_sel mgs.data
execute store result score @s mgs.zb.pap_mid run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
execute as @n[tag=bs.interaction.target] at @s run function mgs:v5.0.0/zombies/pap/anim/start with storage mgs:temp _pap
tag @s remove mgs.pap_owner

