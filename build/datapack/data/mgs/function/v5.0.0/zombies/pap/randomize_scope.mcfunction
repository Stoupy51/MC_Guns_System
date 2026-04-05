
#> mgs:v5.0.0/zombies/pap/randomize_scope
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap_extract.stats
#
# @args		base_weapon (unknown)
#

data remove storage mgs:temp _pap_scopes
$data modify storage mgs:temp _pap_scopes set from storage mgs:zombies scope_variants."$(base_weapon)"

# Skip if weapon has no scope variants or only one
execute unless data storage mgs:temp _pap_scopes[1] run return 0

# Count variants
execute store result score #pap_scope_count mgs.data run data get storage mgs:temp _pap_scopes

# Pick random index: random 0..999999 then modulo count
execute store result score #pap_scope_idx mgs.data run random value 0..999999
scoreboard players operation #pap_scope_idx mgs.data %= #pap_scope_count mgs.data

# Iterate to the picked index
scoreboard players set #pap_scope_i mgs.data 0
data modify storage mgs:temp _pap_scope_pick set from storage mgs:temp _pap_scopes[0]
execute if score #pap_scope_i mgs.data < #pap_scope_idx mgs.data run function mgs:v5.0.0/zombies/pap/scope_pick_advance

# Apply the picked scope to the weapon extract
data modify storage mgs:temp _pap_extract.stats.models.normal set from storage mgs:temp _pap_scope_pick.model
data modify storage mgs:temp _pap_extract.stats.models.zoom set from storage mgs:temp _pap_scope_pick.zoom
data modify storage mgs:temp _pap_extract.weapon set from storage mgs:temp _pap_scope_pick.id
data remove storage mgs:temp _pap_extract.stats.scope_level
execute if data storage mgs:temp _pap_scope_pick.scope_level run data modify storage mgs:temp _pap_extract.stats.scope_level set from storage mgs:temp _pap_scope_pick.scope_level

