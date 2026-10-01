
#> mgs:v5.1.0/zombies/pap/apply_camo
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/randomize_camo with storage mgs:temp _pap_camo_data
#
# @args		weapon_id (unknown)
#			camo (unknown)
#

# Macro: $(weapon_id) after the scope pick, $(camo) the camo name.
$data modify storage mgs:temp _pap_extract.stats.models.normal set value "mgs:$(weapon_id)_$(camo)"
$data modify storage mgs:temp _pap_extract.stats.models.zoom set value "mgs:$(weapon_id)_$(camo)_zoom"

