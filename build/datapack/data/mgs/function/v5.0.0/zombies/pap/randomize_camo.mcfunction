
#> mgs:v5.0.0/zombies/pap/randomize_camo
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/repap_scope_only with storage mgs:temp _pap_extract.stats
#			mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap_extract.stats
#
# @args		base_weapon (unknown)
#

# MACRO: $(base_weapon) from _pap_extract.stats
data modify storage mgs:temp _pap_camos set value []
$data modify storage mgs:temp _pap_camos set from storage mgs:zombies camo_variants."$(base_weapon)"
execute unless data storage mgs:temp _pap_camos[0] run data modify storage mgs:temp _pap_camos set from storage mgs:zombies camo_variants._default
execute unless data storage mgs:temp _pap_camos[0] run return 0

# Pick a random camo variant using Bookshelf
data modify storage bs:in random.choice.options set from storage mgs:temp _pap_camos
function #bs.random:choice
data modify storage mgs:temp _pap_camo_pick set from storage bs:out random.choice

# Build apply data: post-scope weapon id + picked camo name
data modify storage mgs:temp _pap_camo_data set value {}
data modify storage mgs:temp _pap_camo_data.camo set from storage mgs:temp _pap_camo_pick

# Fallback to base weapon id when no scoped weapon id is present
data modify storage mgs:temp _pap_camo_data.weapon_id set from storage mgs:temp _pap_extract.stats.base_weapon
execute if data storage mgs:temp _pap_extract.weapon run data modify storage mgs:temp _pap_camo_data.weapon_id set from storage mgs:temp _pap_extract.weapon
function mgs:v5.0.0/zombies/pap/apply_camo with storage mgs:temp _pap_camo_data

