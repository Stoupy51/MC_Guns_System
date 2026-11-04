
#> mgs:v5.3.0/zombies/pap/annotate_append_int
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zombies/pap/annotate_int_delta with storage mgs:temp _pap_ann
#			mgs:v5.3.0/zombies/pap/annotate_pct_delta with storage mgs:temp _pap_ann
#
# @args		index (unknown)
#			value (unknown)
#			suffix (unknown)
#

$data modify storage mgs:temp _pap_extract.lore[$(index)].extra append value {"text":" > $(value)$(suffix)","color":"aqua","italic":false}

