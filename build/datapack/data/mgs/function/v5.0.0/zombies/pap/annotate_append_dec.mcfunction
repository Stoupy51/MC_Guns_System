
#> mgs:v5.0.0/zombies/pap/annotate_append_dec
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/annotate_time_delta with storage mgs:temp _pap_ann
#			mgs:v5.0.0/zombies/pap/annotate_rate_delta with storage mgs:temp _pap_ann
#
# @args		index (unknown)
#			whole (unknown)
#			dec (unknown)
#			suffix (unknown)
#

$data modify storage mgs:temp _pap_extract.lore[$(index)].extra append value {"text":" > $(whole).$(dec)$(suffix)","color":"aqua","italic":false}

