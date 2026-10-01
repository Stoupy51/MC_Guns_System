
#> mgs:v5.1.0/zombies/pap/randomize_scope
#
# @within	mgs:v5.1.0/zombies/pap/randomize_scope_different with storage mgs:temp _pap_extract.stats
#			mgs:v5.1.0/zombies/pap/on_right_click with storage mgs:temp _pap_extract.stats
#			mgs:v5.1.0/zombies/pap/upgrade_core with storage mgs:temp _pap_extract.stats
#
# @args		base_weapon (unknown)
#

data remove storage mgs:temp _pap_scopes
$data modify storage mgs:temp _pap_scopes set from storage mgs:zombies scope_variants."$(base_weapon)"

# Nothing to pick with fewer than 2 variants.
execute unless data storage mgs:temp _pap_scopes[1] run return 0

data modify storage bs:in random.choice.options set from storage mgs:temp _pap_scopes
function #bs.random:choice
data modify storage mgs:temp _pap_scope_pick set from storage bs:out random.choice

data modify storage mgs:temp _pap_extract.stats.models.normal set from storage mgs:temp _pap_scope_pick.model
data modify storage mgs:temp _pap_extract.stats.models.zoom set from storage mgs:temp _pap_scope_pick.zoom
data modify storage mgs:temp _pap_extract.weapon set from storage mgs:temp _pap_scope_pick.id
data remove storage mgs:temp _pap_extract.stats.scope_level
execute if data storage mgs:temp _pap_scope_pick.scope_level run data modify storage mgs:temp _pap_extract.stats.scope_level set from storage mgs:temp _pap_scope_pick.scope_level

