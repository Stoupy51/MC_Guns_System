
#> mgs:v5.0.0/zombies/pap/randomize_scope_different
#
# @within	mgs:v5.0.0/zombies/pap/randomize_scope_different
#			mgs:v5.0.0/zombies/pap/repap_scope_only with storage mgs:temp _pap_extract.stats
#			mgs:v5.0.0/zombies/pap/free_scope_reroll with storage mgs:temp _pap_extract.stats
#
# @args		base_weapon (unknown)
#

# Skip if weapon has no scope variants or only one (default)
$data modify storage mgs:temp _pap_scopes set from storage mgs:zombies scope_variants."$(base_weapon)"
execute unless data storage mgs:temp _pap_scopes[1] run return 0

# Randomize scope again
function mgs:v5.0.0/zombies/pap/randomize_scope with storage mgs:temp _pap_extract.stats

# data modify set returns 0 if values are equal, 1 if different
execute store success score #pap_scope_changed mgs.data run data modify storage mgs:temp _pap_old_weapon set from storage mgs:temp _pap_extract.weapon

# Retry if same weapon ID was picked (guaranteed to terminate since ≥2 variants exist)
execute if score #pap_scope_changed mgs.data matches 0 run function mgs:v5.0.0/zombies/pap/randomize_scope_different

