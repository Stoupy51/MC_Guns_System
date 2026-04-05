
#> mgs:v5.0.0/zombies/pap/annotate_append_int
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/annotate_int_delta with storage mgs:temp _pap_ann
#			mgs:v5.0.0/zombies/pap/annotate_pct_delta with storage mgs:temp _pap_ann
#
# @args		index (unknown)
#			value (unknown)
#			suffix (unknown)
#

$data modify storage mgs:temp _pap_extract.lore[$(index)].extra append value {"text":" > $(value)$(suffix)","color":"aqua","italic":false}

