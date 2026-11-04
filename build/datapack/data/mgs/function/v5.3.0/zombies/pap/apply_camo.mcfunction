
#> mgs:v5.3.0/zombies/pap/apply_camo
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/pap/randomize_camo with storage mgs:temp _pap_camo_data
#
# @args		weapon_id (unknown)
#			camo (unknown)
#

# Macro: $(weapon_id) after the scope pick, $(camo) the camo name.
$data modify storage mgs:temp _pap_extract.stats.models.normal set value "mgs:$(weapon_id)_$(camo)"
$data modify storage mgs:temp _pap_extract.stats.models.zoom set value "mgs:$(weapon_id)_$(camo)_zoom"

